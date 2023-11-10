import json
from courses import Course


class CoursesConfig:
    def __init__(self, path, term):
        self.path = path
        self.term = term
        self.courses = self.__build_course_list()

    def __build_course_list(self):
        # Load the config file
        with open(self.path, "r") as file:
            config_data = json.load(file)

        # Build the list of tuples (Course object, email)
        courses = [
            (Course(course_id, self.term), email)
            for email, course_ids in config_data.items()
            for course_id in course_ids
        ]
        return courses

    def remove_course(self, course_id):
        # Load the config file
        with open(self.path, "r") as file:
            config_data = json.load(file)

        # Remove the course from the config data
        updated = False
        for email, course_ids in config_data.items():
            if course_id in course_ids:
                course_ids.remove(course_id)
                updated = True

                # Remove the email key if it has no more course ids
                if not course_ids:
                    del config_data[email]
                break

        # Update the courses list by rebuilding it
        self.courses = self.__build_course_list()

        # Write the updated config back to the file if any changes were made
        if updated:
            with open(self.path, "w") as file:
                json.dump(config_data, file, indent=4)
