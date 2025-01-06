import requests


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

    def send(self, topic: str) -> None:
        """
        Sends a push notification to the specified ntfy topic.

        Args:
            topic (str): The ntfy topic to which the push notification is sent.
        """
        message = f"{self.info}: {self.title}"
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=message.encode("utf-8"),
        )

        print(f"Sent ntfy push to topic '{topic}'")

    def run(self, topic: str) -> None:
        """
        Continuously checks the status and sends a push notification if the status_check returns True.

        Args:
            topic (str): The ntfy topic to which the push notification is sent.
        """
        while not self.status_check():
            continue
        self.send(topic)

    def run_async(self, topic: str) -> None:
        """
        Sends a push notification asynchronously if the status_check returns True.

        Args:
            topic (str): The ntfy topic to which the push notification is sent.
        """
        if self.status_check():
            self.send(topic)

    def run_force(self, topic: str) -> None:
        """
        Forcibly sends a push notification regardless of the status_check result.

        Args:
            topic (str): The ntfy topic to which the push notification is sent.
        """
        self.send(topic)
