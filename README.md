# Pulse

## About

A registration aid for [Oscar](https://oscar.gatech.edu). Simple, effective, and customizable. No login necessary. Pulse is a server-side Python application that notifies students when a course spot opens.

## Installation

To use this project, you need Python 3.8+ installed as well as pip on your device.

- Clone the library `git clone https://github.com/ayushgun/pulse`.

- Install the necessary requirements `pip3 install -r requirements.txt`.

## Usage

### Server-side Application

The simplest usage is to simply run `python src/pulse.py [SEASON] [CRN CONFIG].` in the CLI.
For the season, use 'spring', 'fall', or 'summer'. An example call is below

```sh
user@computer:~$ python src/pulse.py fall crns.json
```

### API

```python
from courses import Course
from tracker import WaitlistNotifier

myCourse = Course(crn, 'fall')
notif = WaitlistNotifier(myCourse)

notif.run()
```

To run it, just do `python path/to/file.py`.

### Info

From the CLI, run `python src/info.py [SEASON] CRN-1 CRN-2 ...` and a notification will be sent
containing information for the class. This does not loop, unlike the tracker.
