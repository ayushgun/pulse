import json

import emails

# Read in SMTP configuration data
with open("smtp.json", "r") as file:
    config_data = json.load(file)


class Notifier:
    @staticmethod
    def __always_true() -> bool:
        """
        A static method that always returns True.
        Used as a default state check function.

        Returns:
            bool: Always True.
        """
        return True

    def __init__(self, title: str, info: str, state=__always_true) -> None:
        """
        Initializes a Notifier object.

        Args:
            title (str): The title of the notification.
            info (str): Additional information for the notification.
            state (Callable[[], bool], optional): A callable that returns a boolean. Defaults to __always_true.
        """

        self.title = title
        self.info = info
        self.status_check = state

    def send(self, email: str) -> None:
        """
        Sends an email notification.

        Args:
            email (str): The recipient's email address.
        """

        message = emails.Message(
            subject="PulseGT: Course Spot Found",
            mail_from=config_data["email"],
            text=f"{self.info}: {self.title}",
        )
        message.send(
            to=email,
            smtp={
                "host": "smtp.gmail.com",
                "tls": True,
                "port": 587,
                "user": config_data["email"],
                "password": config_data["password"],
            },
        )

        print(f"Sent email to {email}")

    def run(self, email: str) -> None:
        """
        Continuously checks the status and sends an email if the status_check returns True.

        Args:
            email (str): The recipient's email address.
        """

        while not self.status_check():
            continue
        self.send(email)

    def run_async(self, email: str) -> None:
        """
        Sends an email asynchronously if the status_check returns True.

        Args:
            email (str): The recipient's email address.
        """

        if self.status_check():
            self.send(email)

    def run_force(self, email: str) -> None:
        """
        Forcibly sends an email regardless of the status_check result.

        Args:
            email (str): The recipient's email address.
        """

        self.send(email)
