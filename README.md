<div align="center">
  
# 🤖 Многофункциональный Telegram-бот
### С анализатором тональности сообщений

**Командная разработка Telegram-бота для анализа текста с использованием готовых ML-моделей и внешних API**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-4.14-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Hugging Face](https://img.shields.io/badge/🤗_Transformers-4.36-FFD21E?style=for-the-badge)](https://huggingface.co)

</div>

---

## 📋 Содержание
- [🌟 О проекте](#-о-проекте)
- [✨ Функциональные возможности](#-функциональные-возможности)
- [⚙️ Детальная реализация](#-детальная-реализация)
- [🛠 Стек технологий](#-стек-технологий)
- [👥 Команда проекта](#-команда-проекта)

---

## 🌟 О проекте

Данный проект представляет собой **Telegram-бота** с функцией анализа тональности сообщений (sentiment analysis). Бот обрабатывает входящие сообщения пользователей, классифицируя их эмоциональную окраску, а также предоставляет дополнительные сервисы через внешние API.

Проект разработан в рамках учебной задачи по **командной разработке** с использованием **Git** и **GitHub**, что позволило отработать навыки совместной работы над кодом, ведения документации и управления версиями.

---

## ✨ Функциональные возможности

| № | Возможность | Краткое описание |
|:-:|:---|:---|
| 1 | **Анализ тональности** | Определение эмоциональной окраски текста с помощью RuBERT |
| 2 | **Интерактивное меню** | Удобная навигация с помощью инлайн-кнопок |
| 3 | **Курсы валют** | Получение актуальных курсов через резервные API |
| 4 | **GigaChat интеграция** | Доступ к нейросетевой модели от Сбера |

---

## ⚙️ Детальная реализация

### 1. 🤖 Telegram-бот
Проект полностью соответствует техническому заданию и включает в себя:
- ✅ Команды `/start`, `/help`, `/status`
- ✅ Обработка текстовых сообщений
- ✅ Интерактивные клавиатуры (inline-кнопки)
- ✅ Отказоустойчивая обработка ошибок

**Внешний вид меню бота:**
![Интерфейс Telegram-бота](image.png)

### 2. 🧠 Модель для анализа тональности
| Параметр | Значение |
|:---|:---|
| **Модель** | `blanchefort/rubert-base-cased-sentiment-rusentiment` |
| **Тип** | RuBERT (Russian BERT) |
| **Задача** | Многоклассовая классификация тональности |
| **Классы** | POSITIVE, NEGATIVE, NEUTRAL |

<details>
<summary><b>📊 Подробное описание модели трансформера</b></summary>
<br>
  
  🤖 **Модель трансформера: RuBERT для анализа тональности**

  **Название модели:** `blanchefort/rubert-base-cased-sentiment-rusentiment`

  **Описание модели:**
  Это специализированная версия RuBERT (Russian BERT), дообученная на корпусе RuSentiment для задачи анализа тональности (sentiment analysis) русскоязычных текстов.

  **Решаемая задача:**
  Классификация текста по тональности (многоклассовая классификация)
</details>

### 3. 🌐 Используемые API

<details>
<summary><b>🤖 GigaChat API (Сбер)</b></summary>
<br>
  
  **Название:** GigaChat API от Сбера (Внешнее API Сбера для доступа к модели GigaChat)

  **Описание:**
  API для взаимодействия с языковой моделью GigaChat, предоставляющей возможности генерации текста, ответов на вопросы и выполнения различных задач на естественном языке.

</details>

<details>
<summary><b>💱 API для получения курсов валют</b></summary>
<br>
  
  В проекте реализована **отказоустойчивая система** с тремя резервными API:

  **2.1 ЦБ РФ (Центральный Банк России)**
  - Эндпоинт: `https://www.cbr-xml-daily.ru/daily_json.js`
  - Описание: Официальный API Центрального банка России, предоставляющий курсы валют по отношению к рублю. Самый надежный источник для операций с рублем.


  **2.2 exchangerate-api.com**
  - Эндпоинт: `https://api.exchangerate-api.com/v4/latest/{BASE_CURRENCY}`
  - Описание: Бесплатное API для получения актуальных курсов валют. Не требует ключа, имеет ограничения на количество запросов.

  **2.3 freecurrencyapi.com**
  - Эндпоинт: `https://api.freecurrencyapi.com/v1/latest`
  - Описание: Резервное API для получения курсов валют. Также не требует ключа.

</details>

### 4. 📊 Подтверждение работы с Git/GitHub

![На этом этапе были проблемы](image-1.png)

---

## 🛠 Стек технологий

<div align="center">

| Категория | Технологии |
|:---|:---|
| **Язык программирования** | ![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white) |
| **Telegram Bot** | ![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-4.14-26A5E4?style=flat-square&logo=telegram&logoColor=white) |
| **Machine Learning** | ![Transformers](https://img.shields.io/badge/🤗_Transformers-4.36-FFD21E?style=flat-square) ![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) |
| **Внешние API** | ![REST API](https://img.shields.io/badge/REST_API-Integration-25A162?style=flat-square&logo=fastapi&logoColor=white) |
| **Версионирование** | ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white) |

</div>

---

## 👥 Команда проекта

<div align="center">
  <table>
    <tr>
      <td align="center" width="200">
        <a href="https://github.com/mewkfeli">
          <img src="https://github.com/mewkfeli.png" width="100" style="border-radius:50%" alt="mewkfeli"/><br />
          <b>@mewkfeli</b>
        </a>
        <br />
        <sub>🧠 ML-инженер / Backend</sub>
        <br />
        <sub>• Разработка API для модели ИИ<br/>• Интеграция трансформера<br/>• Написание клиента для внешнего API<br/>• Интеграция с ботом</sub>
      </td>
      <td align="center" width="200">
        <a href="https://github.com/eyeelwhy">
          <img src="https://github.com/eyeelwhy.png" width="100" style="border-radius:50%" alt="eyeelwhy"/><br />
          <b>@eyeelwhy</b>
        </a>
        <br />
        <sub>🤖 Telegram Bot Developer</sub>
        <br />
        <sub>• Разработка Telegram-бота<br/>• Создание клавиатур и обработчиков<br/>• Интеграция с API</sub>
      </td>
    </tr>
  </table>
</div>

---

<div align="center">
  
  **Проект разработан в рамках учебной практики по командной разработке**  
  [⬆️ Вернуться к началу](#-многофункциональный-telegram-бот)

</div>
