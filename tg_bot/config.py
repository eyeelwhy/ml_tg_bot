import os

API_URL = "http://127.0.0.1:8000"
# токен Telegram бота
BOT_TOKEN = "8703862159:AAHpwoDpmnsRE94CSZXvTbuVE8wQtr7-6IQ"

MAIN_CURRENCIES = {
    'USD': '🇺🇸 Доллар США',
    'EUR': '🇪🇺 Евро',
    'RUB': '🇷🇺 Российский рубль',
    'GBP': '🇬🇧 Британский фунт',
    'JPY': '🇯🇵 Японская иена',
    'CNY': '🇨🇳 Китайский юань',
    'CHF': '🇨🇭 Швейцарский франк',
    'CAD': '🇨🇦 Канадский доллар',
    'AUD': '🇦🇺 Австралийский доллар',
    'TRY': '🇹🇷 Турецкая лира'
}

CURRENCY_CODES = list(MAIN_CURRENCIES.keys())