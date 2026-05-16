import os


def notify(body):
    msg = Message(
        subject="moBay notification,
        recipients=[os.environ.get("ADMIN_EMAIL")]
    )
    msg.body = body
    mail.send(msg)
