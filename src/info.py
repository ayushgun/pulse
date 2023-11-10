import sys
from datetime import datetime
from typing import List

from courses import Course
from tracker import CourseList


def get_term(season: str, current_date: datetime) -> str:
    """
    Determines the term code based on the given season and current date.

    Args:
        season (str): The desired season (Spring, Summer, or Fall).
        current_date (datetime): The current date and time.

    Returns:
        str: The term code corresponding to the season.
    """

    year = current_date.year

    if season.lower() == "spring":
        return f"{year + 1}02" if current_date.month > 4 else f"{year}02"
    elif season.lower() == "summer":
        return f"{year}05"
    elif season.lower() == "fall":
        return f"{year}08"

    raise ValueError("Season must be either spring, summer, or fall")


def create_course_list(crns: List[str], term: str) -> CourseList:
    """
    Creates a list of Course objects based on the provided CRNs and term.

    Args:
        crns (List[str]): A list of Course Registration Numbers.
        term (str): The term code.

    Returns:
        CourseList: A CourseList object containing the created Course objects.
    """

    courses = [Course(crn, term) for crn in crns]
    return CourseList(courses)


def main() -> None:
    """
    Main function to execute the script.
    """

    if len(sys.argv) < 3:
        print(
            "Could not run Pulse; include the desired upcoming term (Fall, Spring, Summer) and use at least one CRN"
        )
        sys.exit(1)

    season = sys.argv[1]
    now = datetime.now()
    term = get_term(season, now)

    crns = sys.argv[2:]
    course_list = create_course_list(crns, term)
    course_list.get_info()


if __name__ == "__main__":
    main()
