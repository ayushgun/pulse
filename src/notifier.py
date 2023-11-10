import emails
import json

# Read in SMTP config data
with open("smtp.json") as file:
    config_data = json.load(file)


class Notifier:
    def __always_true():
        return True

    def __init__(self, title: str, info: str, state=__always_true):
        self.title, self.info = title, info
        self.status_check = state

    def send(self, email):
        emails.Message(
            subject="Course Sniper -- Your Course Is Open",
            mail_from=config_data["email"],
            text=f"{self.info}: {self.title}",
        ).send(
            to=email,
            smtp={
                "host": "smtp.gmail.com",
                "tls": True,
                "user": config_data["email"],
                "password": config_data["password"],
            },
        )

        print(f"Sent email to {email}")

    def run(self, email):
        while not self.status_check():
            continue
        self.send(email)

    def run_async(self, email):
        if self.status_check():
            self.send(email)

    def run_force(self, email):
        self.send(email)
