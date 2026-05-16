import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")


def notify(message):
    try:
        resend.Emails.send({
            "from": "Meu Site mobay",
            "to": os.getenv("ADMIN_EMAIL"),
            "subject": "Notificação do site",
            "text": message
        })
    except Exception as e:
        return f"Erro email: {e}"
