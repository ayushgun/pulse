import sys
from datetime import datetime
import time

from config import CoursesConfig
from info import get_term
from tracker import CourseList


def main() -> None:
    """
    Main function to run the course notifier.
    """
    if len(sys.argv) < 3:
        print(
            "Could not run Pulse; include the desired upcoming term (Fall, Spring, Summer) and provide the config path"
        )
        sys.exit(1)

    season = sys.argv[1]
    now = datetime.now()
    term = get_term(season, now)

    path = sys.argv[2]
    config = CoursesConfig(path, term)
    lst = CourseList(config)
    lst.run_notifiers()


# Auto-restart loop
while True:
    try:
        if __name__ == "__main__":
            main()
    except Exception as e:
        print(f"Script crashed with exception: {e}")
        print("Restarting the script...")
        time.sleep(5)  # Wait 5 seconds before restarting
