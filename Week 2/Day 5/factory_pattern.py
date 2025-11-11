from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """
        Sends notification message
        Args:
            message: content to send
        """
        pass


class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"sending email notification message: {message}")


class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"sending SMS notification message: {message}")


class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"sending push notification message: {message}")


class NotificationFactory:
    def create_notification(self, type: str) -> Notification:
        """
        creates a Notification instance based on given type
        Args:
            type: type to notification to create
        """
        if type == "email":
            return EmailNotification()
        elif type == "sms":
            return SMSNotification()
        elif type == "push":
            return PushNotification()
        else:
            raise Exception(f"Notification type - {type} - unrecognized")


if __name__ == "__main__":
    noti_factory = NotificationFactory()

    sms_noti = noti_factory.create_notification("sms")
    email_noti = noti_factory.create_notification("email")
    push_noti = noti_factory.create_notification("push")
    inv_noti = noti_factory.create_notification("pushing")

    sms_noti.send("Hellllllllo")
