import requests
import os

def notify(message):

    url = os.getenv("EMAIL_SERVICE_URL")  # URL do teu servidor

    try:
        requests.get(
            f"http://idmz.pythonanywhere.com/Ola+do+render"
        )
    except Exception as e:
        print("Erro email service:", e)
