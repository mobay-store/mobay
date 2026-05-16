from flask_mail import Message
from flask import current_app

def notify(message):
    try:
        mail = current_app.extensions["mail"]

        msg = Message(
            subject="moBay notification",
            recipients=[current_app.config["MAIL_USERNAME"]]
        )

        msg.body = message

        mail.send(msg)

        print("EMAIL ENVIADO")

    except Exception as e:
        print("ERRO EMAIL:", e)
