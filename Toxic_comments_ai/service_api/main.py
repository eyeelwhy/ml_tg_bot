import os
import nltk
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np
from pymorphy3 import MorphAnalyzer
from nltk.corpus import stopwords
from keras.preprocessing.sequence import pad_sequences
import pymysql
from datetime import datetime
import json
import uuid
import requests
from typing import Optional, Dict, Any, List
import uvicorn

DB_CONFIG = {
    'host': 'localhost',
    'database': 'comments',
    'user': 'root',
    'password': 'root'
}

GIGACHAT_CREDENTIALS = os.getenv(
    "GIGACHAT_CREDENTIALS",
    "MDE5OWUyZjctYjcxOC03NmIyLTlkYzItYWMxYjk3M2Y2ZWJkOjFjZWNjYTRkLWRjYzYtNDA3Ni1iNmM4LWQ2ZTNhOWI2YzU5Ng=="
)

morph = MorphAnalyzer()
my_stop_words = ["такой", "это", "всё", "весь"]
stop_words = set(stopwords.words('russian'))
stop_words.update(my_stop_words)


class TextRequest(BaseModel):
    text: str


class CommentToneResponse(BaseModel):
    text: str
    predictions: dict
    is_toxic: bool
    dominant_tone: str


class GigaChatRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.1


class GigaChatResponse(BaseModel):
    response: str


class CurrencyRequest(BaseModel):
    base_currency: str = "USD"
    target_currency: str = "RUB"
    amount: Optional[float] = 1.0


class CurrencyRateResponse(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    converted_amount: float
    last_updated: str
    source: str


class AllRatesResponse(BaseModel):
    base_currency: str
    rates: Dict[str, float]
    last_updated: str
    source: str


def full_preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    words = [t.replace('ё', 'е') for t in tokens if t.isalpha()]
    lemmas = [morph.parse(w)[0].normal_form for w in words]
    filtered_lemmas = [l for l in lemmas if l not in stop_words]
    return filtered_lemmas


class GigaChatClient:
    def __init__(self):
        self.auth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.chat_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        self.credentials = GIGACHAT_CREDENTIALS

    def get_access_token(self) -> str:
        try:
            headers = {
                "Authorization": f"Basic {self.credentials}",
                "RqUID": str(uuid.uuid4()),
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {"scope": "GIGACHAT_API_PERS"}
            response = requests.post(
                self.auth_url,
                headers=headers,
                data=data,
                verify=False,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            print(f"❌ Ошибка получения токена GigaChat: {e}")
            raise Exception(f"Ошибка авторизации GigaChat: {str(e)}")

    def send_prompt(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.1) -> str:
        try:
            access_token = self.get_access_token()
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "GigaChat",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1000,
                "stream": False
            }
            response = requests.post(
                self.chat_url,
                headers=headers,
                json=payload,
                verify=False,
                timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"Ошибка GigaChat API: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка запроса к GigaChat: {e}")
            raise Exception(f"Ошибка GigaChat: {str(e)}")


def get_currency_rate_cbr_api(base: str, target: str, amount: float = 1.0) -> Dict[str, Any]:
    """API Центробанка России (самый надежный для RUB)"""
    try:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = data['Valute']

        if base == 'RUB' and target == 'RUB':
            rate = 1.0
            converted = amount
        elif base == 'RUB':
            if target in rates:
                rate = 1 / rates[target]['Value']
                converted = amount * rate
            else:
                raise Exception(f"Валюта {target} не найдена")
        elif target == 'RUB':
            if base in rates:
                rate = rates[base]['Value']
                converted = amount * rate
            else:
                raise Exception(f"Валюта {base} не найдена")
        else:
            if base in rates and target in rates:
                rate = rates[base]['Value'] / rates[target]['Value']
                converted = amount * rate
            else:
                raise Exception("Одна из валют не найдена")

        return {
            "rate": rate,
            "converted": converted,
            "date": data['Date'][:10]
        }
    except Exception as e:
        print(f"❌ Ошибка CBR API: {e}")
        raise Exception(f"CBR API error: {str(e)}")


def get_currency_rate_exchangerate_api(base: str, target: str, amount: float = 1.0) -> Dict[str, Any]:
    """API exchangerate-api.com"""
    url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if target.upper() in data["rates"]:
        rate = data["rates"][target.upper()]
        return {
            "rate": rate,
            "converted": amount * rate,
            "date": data["date"]
        }
    raise Exception("exchangerate-api.com вернул ошибку")


def get_currency_rate_freecurrency_api(base: str, target: str, amount: float = 1.0) -> Dict[str, Any]:
    """API freecurrencyapi.com (бесплатный ключ не требуется)"""
    url = f"https://api.freecurrencyapi.com/v1/latest"
    params = {
        "base_currency": base.upper(),
        "currencies": target.upper()
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("data") and target.upper() in data["data"]:
        rate = data["data"][target.upper()]
        return {
            "rate": rate,
            "converted": amount * rate,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    raise Exception("freecurrencyapi.com вернул ошибку")


def get_currency_rate(base: str, target: str, amount: float = 1.0) -> Dict[str, Any]:
    """
    Получение курса валют с несколькими попытками через разные API
    """
    errors = []

    apis = [
        ("ЦБ РФ", get_currency_rate_cbr_api),
        ("exchangerate-api.com", get_currency_rate_exchangerate_api),
        ("freecurrencyapi.com", get_currency_rate_freecurrency_api)
    ]

    for api_name, api_func in apis:
        try:
            print(f"🔄 Пробуем API: {api_name}")
            result = api_func(base, target, amount)
            print(f"✅ Успешно через {api_name}")
            result["source"] = api_name
            return result
        except Exception as e:
            error_msg = f"{api_name}: {str(e)}"
            print(f"❌ Ошибка {error_msg}")
            errors.append(error_msg)
            continue

    error_text = "; ".join(errors)
    raise Exception(f"Не удалось получить курс валют. Ошибки: {error_text}")


def get_all_rates(base: str) -> Dict[str, Any]:
    """
    Получение всех курсов для базовой валюты
    """
    try:
        if base == 'RUB':
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            rates = {}
            for code, val in data['Valute'].items():
                rates[code] = val['Value']

            return {
                "rates": rates,
                "date": data['Date'][:10]
            }
        else:
            url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "rates": data["rates"],
                "date": data["date"]
            }
    except Exception as e:
        print(f"❌ Ошибка получения всех курсов: {e}")
        raise Exception(f"Не удалось получить курсы валют: {str(e)}")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Загрузка модели...")
try:
    model = tf.keras.models.load_model('lstm_model.h5')
    print("✅ Модель загружена")
except Exception as e:
    print(f"❌ Ошибка загрузки модели: {e}")
    model = None

print("Загрузка токенизатора...")
try:
    with open('tokenizer.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    print("✅ Токенизатор загружен")
except Exception as e:
    print(f"❌ Ошибка загрузки токенизатора: {e}")
    tokenizer = None

target_names = ['normal', 'insult', 'threat', 'obscenity']
gigachat_client = GigaChatClient()


@app.post("/analyze-comment", response_model=CommentToneResponse)
async def analyze_comment(request: TextRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Модель не загружена")

    clean_text = full_preprocess(request.text)
    seq = tokenizer.texts_to_sequences([clean_text])
    # Выравнивание последовательностей до одинаковой длины (100 токенов)
    padded = pad_sequences(seq, maxlen=100)
    pred = model.predict(padded, verbose=0)[0]

    predictions = {target_names[i]: float(pred[i]) for i in range(len(target_names))}
    is_toxic = any(predictions[label] > 0.5 for label in target_names if label != 'normal')
    dominant_tone = max(predictions, key=predictions.get)

    return CommentToneResponse(
        text=request.text,
        predictions=predictions,
        is_toxic=is_toxic,
        dominant_tone=dominant_tone
    )


@app.post("/gigachat/ask", response_model=GigaChatResponse)
async def ask_gigachat(request: GigaChatRequest):
    try:
        response_text = gigachat_client.send_prompt(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            temperature=request.temperature
        )
        return GigaChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/currency/convert", response_model=CurrencyRateResponse)
async def convert_currency(request: CurrencyRequest):
    """
    Конвертация валют с использованием нескольких бесплатных API
    """
    try:
        result = get_currency_rate(
            base=request.base_currency,
            target=request.target_currency,
            amount=request.amount
        )

        return CurrencyRateResponse(
            base_currency=request.base_currency.upper(),
            target_currency=request.target_currency.upper(),
            rate=result["rate"],
            converted_amount=result["converted"],
            last_updated=result["date"],
            source=result.get("source", "Multiple APIs")
        )

    except Exception as e:
        print(f"❌ Ошибка конвертации валют: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/currency/rates/{base_currency}", response_model=AllRatesResponse)
async def get_all_currency_rates(base_currency: str):
    """
    Получение всех курсов для базовой валюты
    """
    try:
        result = get_all_rates(base_currency)

        return AllRatesResponse(
            base_currency=base_currency.upper(),
            rates=result["rates"],
            last_updated=result["date"],
            source="CBR / exchangerate-api.com"
        )
    except Exception as e:
        print(f"❌ Ошибка получения курсов: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/currency/list")
async def get_supported_currencies():
    """
    Список поддерживаемых валют
    """
    currencies = {
        "USD": "🇺🇸 Доллар США",
        "EUR": "🇪🇺 Евро",
        "RUB": "🇷🇺 Российский рубль",
        "GBP": "🇬🇧 Британский фунт",
        "JPY": "🇯🇵 Японская иена",
        "CNY": "🇨🇳 Китайский юань",
        "CHF": "🇨🇭 Швейцарский франк",
        "CAD": "🇨🇦 Канадский доллар",
        "AUD": "🇦🇺 Австралийский доллар",
        "TRY": "🇹🇷 Турецкая лира",
        "KZT": "🇰🇿 Казахстанский тенге",
        "BYN": "🇧🇾 Белорусский рубль",
        "UAH": "🇺🇦 Украинская гривна",
        "PLN": "🇵🇱 Польский злотый",
        "CZK": "🇨🇿 Чешская крона"
    }
    return {"supported_currencies": currencies}


@app.get("/currency/health")
async def currency_health():
    """
    Проверка доступности API валют
    """
    results = {}

    try:
        result = get_currency_rate_cbr_api("USD", "RUB", 1)
        results["cbr_api"] = "✅ Работает"
    except Exception as e:
        results["cbr_api"] = f"❌ Ошибка: {str(e)}"

    try:
        result = get_currency_rate_exchangerate_api("USD", "RUB", 1)
        results["exchangerate_api"] = "✅ Работает"
    except Exception as e:
        results["exchangerate_api"] = f"❌ Ошибка: {str(e)}"

    return results


@app.get("/")
async def root():
    return {
        "message": "Toxic Comments & GigaChat & Currency API работает",
        "endpoints": {
            "analyze-comment": "POST /analyze-comment - Анализ тональности комментария",
            "gigachat/ask": "POST /gigachat/ask - Запрос к GigaChat",
            "currency/convert": "POST /currency/convert - Конвертация валют",
            "currency/rates/{base}": "GET /currency/rates/USD - Все курсы для валюты",
            "currency/list": "GET /currency/list - Список поддерживаемых валют",
            "currency/health": "GET /currency/health - Проверка API валют"
        },
        "status": "ok"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)