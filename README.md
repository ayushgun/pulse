# Pulse

## About

Pulse is a fast Python application to track open course spots and waitlist availability on [Oscar](https://oscar.gatech.edu). It sends push notifications when spots open.

## Installation

**Requirements:** Python 3.8+, `pip`. 

**Steps:** 
1. Clone the repository: `git clone https://github.com/ayushgun/pulse`.
2. Install dependencies: `pip3 install -r requirements.txt`.

## Usage

### Running the Tracker

Run: `python src/pulse.py [SEASON] [CRN CONFIG]`. **Arguments:** `SEASON` (e.g., `spring`, `fall`, `summer`), `CRN CONFIG` (path to JSON with CRNs and ntfy topics). **Example:** `python src/pulse.py fall crns.json`.

**Config File Example (crns.json):**

```json
{
  "george-p-burdell-alerts": ["31234", "34567"],
}
```

In this example: `george-p-burdell-alerts` is a [ntfy](https://ntfy.sh/) topic. **CRNs** are listed as values for each topic. When a course spot opens, a push notification is sent to the corresponding topic.

### API Usage

Example:

```python
from courses import Course
from tracker import WaitlistNotifier

my_course = Course("25645", "fall")
notif = WaitlistNotifier(my_course)
notif.run()
```

Run your script: `python path/to/your_script.py`.

### Course Info Command

Run: `python src/info.py [SEASON] CRN-1 CRN-2 ...`. **Example:** `python src/info.py fall 25645 26789 31234`. This sends a one-time notification with course details to the configured ntfy topics. Unlike the tracker, this command does **not** loop.

