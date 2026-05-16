import requests
import os

def notify(message):

    url = os.getenv("EMAIL_SERVICE_URL")  # URL do teu servidor

    try:
        requests.post(
            f"{url}/send-email",
            json={"message": message},
            timeout=5
        )
    except Exception as e:
        print("Erro email service:", e)
