import json

from courses import Course


class CoursesConfig:
    def __init__(self, path: str, term: str) -> None:
        """
        Initialize the CoursesConfig object.

        Args:
            path (str): The file path to the courses configuration file.
            term (str): The term for which courses are being configured.
        """

        self.path = path
        self.term = term
        self.courses = self.__build_course_list()

    def __build_course_list(self) -> list[tuple[Course, str]]:
        """
        Builds a list of courses from the configuration file.

        Each item in the list is a tuple containing a Course object and a ntfy topic string.

        Returns:
            list[tuple[Course, str]]: A list of tuples containing Course objects and corresponding topics.
        """

        # Load the config file
        with open(self.path, "r") as file:
            config_data = json.load(file)

        # Build the list of tuples (Course object, topic)
        courses = [
            (Course(course_id, self.term), topic)
            for topic, course_ids in config_data.items()
            for course_id in course_ids
        ]
        return courses

    def remove_course(self, course_id: str) -> None:
        """
        Removes a course from the configuration by its course ID.

        Args:
            course_id (str): The ID of the course to be removed.
        """

        # Load the config file
        with open(self.path, "r") as file:
            config_data = json.load(file)

        # Remove the course from the config data
        updated = False
        for topic, course_ids in config_data.items():
            if course_id in course_ids:
                course_ids.remove(course_id)
                updated = True

                # Remove the topic key if it has no more course IDs
                if not course_ids:
                    del config_data[topic]
                break

        # Update the courses list by rebuilding it
        self.courses = self.__build_course_list()

        # Write the updated config back to the file if any changes were made
        if updated:
            with open(self.path, "w") as file:
                json.dump(config_data, file, indent=4)
