import requests
from config import API_URL

# _____________________________________________
# Клиент для взаимодействия с backend API.
# _____________________________________________

class APIClient:
    @staticmethod
    def analyze_comment(text):
        """
        отправляет текст на анализ тональности
        """
        response = requests.post(
            f"{API_URL}/analyze-comment",
            json={"text": text},
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def gigachat_request(prompt):
        """
        отправляет запрос к GigaChat
        """
        response = requests.post(
            f"{API_URL}/gigachat/ask",
            json={"prompt": prompt, "temperature": 0.1},
            timeout=60,
            verify=False
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def convert_currency(from_currency, to_currency, amount):
        """
        конвертирует валюты
        """
        response = requests.post(
            f"{API_URL}/currency/convert",
            json={
                "base_currency": from_currency,
                "target_currency": to_currency,
                "amount": amount
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_rates(currency):
        """
        получает курсы валют
        """
        response = requests.get(
            f"{API_URL}/currency/rates/{currency}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()