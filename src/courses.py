import requests
from bs4 import BeautifulSoup


class Course:
    def __init__(self, crn: str, term: str) -> None:
        """
        Initialize a Course object.

        Args:
            crn (str): The course registration number.
            term (str): The term for the course.
        """

        self.crn = crn
        self.term = term
        url = "https://registration.banner.gatech.edu/StudentRegistrationSsb/ssb/searchResults/getClassDetails?term="
        url += self.term + "&courseReferenceNumber=" + self.crn
        with requests.Session() as s:
            with s.get(url) as page:
                soup = BeautifulSoup(page.content, "html.parser")
                title = soup.find("span", id="courseTitle").getText()
                number = soup.find("span", id="courseNumber").getText()
                subject = soup.find("span", id="subject").getText()
                self.name = subject + " " + number + " - " + title

    def __get_registration_info(self, term: str) -> list[int]:
        """
        Fetches registration information for the course.

        Args:
            term (str): The term for which to fetch registration information.

        Returns:
            list[int]: A list containing registration information as integers.
        """

        url = "https://registration.banner.gatech.edu/StudentRegistrationSsb/ssb/searchResults/getEnrollmentInfo?term="
        url += term + "&courseReferenceNumber=" + self.crn

        with requests.Session() as s:
            with s.get(url) as page:
                soup = BeautifulSoup(page.content, "html.parser")
                data = [
                    int(info.getText())
                    for info in soup.find_all("span", dir="ltr")
                ]
                # jank, ayush come up with a better one-liner 
                data[0], data[1] = data[1], data[0]
                return data

    def get_registration_info(self, term: str) -> dict[str, int]:
        """
        Processes and returns the registration information for a course.

        Args:
            term (str): The term for the course.

        Returns:
            dict[str, int]: A dictionary containing processed registration data.
        """

        self.term = term
        data = self.__get_registration_info(term)

        if len(data) < 6:
            raise ValueError()

        waitlist_data = {"seats": data[3], "taken": data[4], "vacant": data[5]}
        load = {
            "seats": data[0],
            "taken": data[1],
            "vacant": data[2],
            "waitlist": waitlist_data,
        }
        return load

    def is_open_by_term(self, term: str) -> bool:
        """
        Checks if the course is open for registration for a specific term.

        Args:
            term (str): The term to check.

        Returns:
            bool: True if the course is open, False otherwise.
        """

        return self.__get_registration_info(term)[2] > 0

    def is_open(self) -> bool:
        """
        Checks if the course is open for registration for the current term.

        Returns:
            bool: True if the course is open, False otherwise.
        """

        return self.is_open_by_term(self.term)

    def waitlist_available_by_term(self, term: str) -> bool:
        """
        Checks if there are available spots on the waitlist for a specific term.

        Args:
            term (str): The term to check.

        Returns:
            bool: True if waitlist spots are available, False otherwise.
        """

        waitlist_data = self.get_registration_info(term)["waitlist"]
        return waitlist_data["vacant"] > 0

    def waitlist_available(self) -> bool:
        """
        Checks if there are available spots on the waitlist for the current term.

        Returns:
            bool: True if waitlist spots are available, False otherwise.
        """

        return self.waitlist_available_by_term(self.term)

    def __str__(self) -> str:
        """
        Returns a string representation of the course, including registration information and waitlist status.

        Returns:
            str: A string representation of the course.
        """

        data = self.get_registration_info(self.term)
        res = "{}\n".format(self.name)
        for name in data:
            if name == "waitlist":
                continue
            res += "{}:\t{}\n".format(name, data[name])
        res += "waitlist open: {}".format(
            "yes" if self.waitlist_available() else "no"
        )
        return res
