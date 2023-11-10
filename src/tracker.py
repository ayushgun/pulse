import sys

from courses import CourseList
from datetime import datetime
from config import CoursesConfig

if len(sys.argv) < 3:
    print(
        "Could not run Pulse; include the desired upcoming term (Fall, Spring, Summer) and provide the config path"
    )
    sys.exit(1)

season = sys.argv[1]
now = datetime.now()
term = ""

if season.lower() == "spring":
    term = f"{now.year + 1}" + "02" if now.month > 4 else f"{now.year}" + "02"
else:
    term = f"{now.year}" + "05" if season.lower() == "summer" else f"{now.year}" + "08"

path = sys.argv[2]
config = CoursesConfig(path, term)
lst = CourseList(config)
lst.run_notifiers()
