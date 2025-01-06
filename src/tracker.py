import time

import config
import notifier
from courses import Course


class WaitlistNotifier(notifier.Notifier):
    def __init__(self, course: Course) -> None:
        """
        Initializes a notifier for waitlist availability.

        Args:
            course (Course): The course object to be monitored for waitlist availability.
        """
        self.title = "Waitlist Available"
        self.info, self.status_check = course.name, course.waitlist_available


class OpenCourseNotifier(notifier.Notifier):
    def __init__(self, course: Course) -> None:
        """
        Initializes a notifier for course availability.

        Args:
            course (Course): The course object to be monitored for open registration.
        """
        self.title = "Course Open"
        self.info, self.status_check = course.name, course.is_open


class CourseList:
    def __init__(self, courses_config: config.CoursesConfig) -> None:
        """
        Initializes a CourseList object.

        Args:
            courses_config (CoursesConfig): The configuration object containing course data.
        """
        self.courses_config = courses_config

    def run_waitlist_notifiers(self) -> None:
        """
        Runs notifiers for all courses with an available waitlist.
        """
        for course, topic in list(self.courses_config.courses):
            if course.waitlist_available():
                notif = WaitlistNotifier(course)
                print(course)
                # Send the push notification to the ntfy topic
                notif.run_async(topic)
                # Remove this course from the config so we don't send multiple pushes
                self.courses_config.remove_course(course.crn)
            time.sleep(3)

    def run_available_courses(self) -> None:
        """
        Runs notifiers for all courses that are currently open for registration.
        """
        for course, topic in list(self.courses_config.courses):
            if course.is_open():
                notif = OpenCourseNotifier(course)
                print(course)
                # Send the push notification to the ntfy topic
                notif.run_async(topic)
                # Remove this course from the config so we don't send multiple pushes
                self.courses_config.remove_course(course.crn)
            time.sleep(5)

    def run_notifiers(self) -> None:
        """
        Continuously runs notifiers for available courses and waitlist spots.
        """
        while self.courses_config.courses:
            # Check for open spots
            self.run_available_courses()

            # (Optional) Uncomment if you also want to monitor waitlists
            # self.run_waitlist_notifiers()

    def get_info(self):
        """
        Prints information for each course in the configuration and sends a forced push.
        """
        cnt = 0
        for course, topic in self.courses_config.courses:
            notif = notifier.Notifier("Info", str(course))
            if cnt > 0:
                print("\n------------------------------------------\n")
            print(course)
            # Force a push so the user sees course info immediately
            notif.run_force(topic)
            cnt += 1
