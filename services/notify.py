import os
from flask_mail import Message

def notify(body):
    msg = Message(
        subject="moBay notification",
        recipients=[os.environ.get("ADMIN_EMAIL")]
    )
    msg.body = body
    mail.send(msg)
