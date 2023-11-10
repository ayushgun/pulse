import re

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
        url = "https://oscar.gatech.edu/bprod/bwckschd.p_disp_detail_sched?term_in="
        url += self.term + "&crn_in=" + self.crn
        with requests.Session() as s:
            with s.get(url) as page:
                soup = BeautifulSoup(page.content, "html.parser")
                headers = soup.find_all("th", class_="ddlabel")
                self.name = headers[0].getText()

    def __get_prereqs(self) -> str:
        """
        Fetches and returns the prerequisites for the course.

        Returns:
            str: A string listing the prerequisites.
        """

        url = "https://oscar.gatech.edu/bprod/bwckschd.p_disp_detail_sched?term_in="
        url += self.term + "&crn_in=" + self.crn

        with requests.Session() as s:
            with s.get(url) as page:
                soup = BeautifulSoup(page.content, "html.parser")
                p = soup.find("td", class_="dddefault")
                txt = p.getText()
                idx = txt.index("Prerequisites:")
                return txt[idx : len(txt) - 4]

    def __is_not_fodder(self, s: str) -> bool:
        """
        Determines if a string is not considered 'fodder' for parsing purposes.

        Args:
            s (str): The string to be evaluated.

        Returns:
            bool: True if the string is not fodder, False otherwise.
        """

        fodder = [
            "undergraduate",
            "graduate",
            "level",
            "grade",
            "of",
            "minimum",
            "semester",
        ]
        tmp = s.lower()
        for fod in fodder:
            if fod == tmp:
                return False
        return True

    def get_prereqs(self) -> str:
        """
        Processes and returns a cleaned and parsed version of prerequisites.

        Returns:
            str: A processed string of prerequisites.
        """

        try:
            raw = self.__get_prereqs()
            block = " ".join(
                list(
                    filter(
                        lambda el: self.__is_not_fodder(el),
                        raw[raw.index("\n") + 3 :].split(),
                    )
                )
            )
            els = re.findall('\[[^\]]*\]|\([^\)]*\)|"[^"]*"|\S+', block)
            parsed = " ".join(els).replace("(Undergraduate ", "(")
            return parsed
        except:
            return "None"

    def __get_registration_info(self, term: str) -> list[int]:
        """
        Fetches registration information for the course.

        Args:
            term (str): The term for which to fetch registration information.

        Returns:
            list[int]: A list containing registration information as integers.
        """

        url = "https://oscar.gatech.edu/bprod/bwckschd.p_disp_detail_sched?term_in="
        url += term + "&crn_in=" + self.crn

        with requests.Session() as s:
            with s.get(url) as page:
                soup = BeautifulSoup(page.content, "html.parser")
                table = soup.find(
                    "caption", string="Registration Availability"
                ).find_parent("table")

                if len(table) == 0:
                    raise ValueError()

                data = [
                    int(info.getText())
                    for info in table.findAll("td", class_="dddefault")
                ]
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
        Returns a string representation of the course, including registration and prerequisite information.

        Returns:
            str: A string representation of the course.
        """

        data = self.get_registration_info(self.term)
        res = "{}\n".format(self.name)
        for name in data:
            if name == "waitlist":
                continue
            res += "{}:\t{}\n".format(name, data[name])
        res += "waitlist open: {}\n".format(
            "yes" if self.waitlist_available() else "no"
        )
        res += "prerequisites: {}".format(self.get_prereqs())
        return res
