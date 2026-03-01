<div align="center">
  
# 🤖 Определитель токсичных комментариев
### Toxic Comments Detector

**Командный проект по созданию Telegram-бота для анализа тональности сообщений с использованием готовой модели ИИ и внешнего API**

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)](https://core.telegram.org/bots/api)
[![Flask](https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Transformers-FFD21E?style=for-the-badge)](https://huggingface.co)

</div>

---

## 🌟 Описание проекта

Проект представляет собой **Telegram-бота**, способного определять токсичность комментариев. Бот анализирует входящие сообщения и классифицирует их по уровню токсичности, используя для этого предобученную модель-трансформер и внешнее API для получения дополнительной информации (например, курса валют по запросу пользователя).

Проект разработан в рамках учебной задачи по **командной разработке** с использованием **Git** и **GitHub**.

### ✨ Ключевые возможности

| № | Возможность | Описание |
|:-:|:---|:---|
| 1 | **Анализ текста** | Определение токсичности отдельного сообщения |
| 2 | **Batch-проверка** | Пакетный анализ нескольких сообщений |
| 3 | **Интерактивные кнопки** | Удобная навигация по меню бота |
| 4 | **Внешнее API** | Получение курса валют по запросу |
| 5 | **ML-модель** | Точное определение тональности с помощью трансформера |

---

## ⚙️ Функциональность

Проект полностью соответствует техническому заданию:

<details>
<summary><b>🤖 Telegram-бот</b></summary>
<br>
  
  - ✅ Приветствие и меню с кнопками (`/start`)
  - ✅ Справка по командам (`/help`)
  - ✅ Команда для проверки статуса бота и API (`/status`)
  - ✅ Обработка текстовых сообщений
  - ✅ Обработка нажатий на инлайн-кнопки
  - ✅ Интерактивные клавиатуры

</details>

<details>
<summary><b>🌐 Внешнее API</b></summary>
<br>
  
  - ✅ Реализован клиент для работы с внешним API (курс валют)
  - ✅ Бот предоставляет актуальные данные по запросу
  - ✅ Обработка ошибок при недоступности API

</details>

<details>
<summary><b>🧠 Готовая модель ИИ (Трансформер)</b></summary>
<br>
  
  - ✅ Используется личная обученная модель для выявления токсичности сообщений
  - ✅ Zero-shot классификация текста без дополнительного обучения
  - ✅ Модель запускается локально в отдельном микросервисе
  - ✅ Быстродействие и независимость от внешних сервисов

</details>

<details>
<summary><b>👥 Командная разработка и Git</b></summary>
<br>
  
  - ✅ Проект разрабатывался двумя участниками
  - ✅ Использование Git с ветвлением (`feature/api`, `feature/tg-bot`)
  - ✅ Код хранится в публичном репозитории на GitHub

</details>

---

## 🛠️ Стек технологий

<div align="center">

| Категория | Технологии |
|:---|:---|
| **Язык программирования** | ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python) |
| **Telegram-бот** | ![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-4.14-26A5E4?logo=telegram) |
| **Веб-фреймворк** | ![Flask](https://img.shields.io/badge/Flask-2.3-000000?logo=flask) ![flask-cors](https://img.shields.io/badge/flask--cors-4.0-000000) |
| **ML / AI** | ![Transformers](https://img.shields.io/badge/Transformers-4.36-FFD21E?logo=huggingface) ![Torch](https://img.shields.io/badge/Torch-2.1-EE4C2C?logo=pytorch) ![GLiClass](https://img.shields.io/badge/GLiClass-1.0-9cf) |
| **HTTP-клиент** | ![Requests](https://img.shields.io/badge/Requests-2.31-007EC6) |
| **Конфигурация** | ![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0-ECD53F) |
| **Контроль версий** | ![Git](https://img.shields.io/badge/Git-F05032?logo=git) ![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github) |

</div>

---

## 📁 Структура проекта

```bash
📦 toxic-comments-detector
├── 📂 tg_bot/                      # Telegram-бот
│   ├── 📄 bot.py                    # Основной файл бота
│   ├── 📄 config.py                 # Конфигурация и переменные окружения
│   ├── 📄 handlers.py               # Обработчики сообщений и колбэков
│   ├── 📄 keyboards.py              # Клавиатуры (Reply/Inline)
│   ├── 📄 api_client.py             # Клиент для внешнего API
│   ├── 📄 utils.py                  # Вспомогательные функции
│   └── 📄 requirements.txt          # Зависимости для бота
├── 📂 Toxic_comments_ai/
│   └── 📂 service_api                # Микросервис на Flask с ML моделью
│       ├── 📄 app.py                    # Flask приложение
│       ├── 📄 model.py                  # Обертка для модели трансформера
│       ├── 📄 requirements.txt          # Зависимости для API
│       └── 📄 README.md                 # Документация API
├── 📄 .gitignore                    # Файлы, игнорируемые Git
└── 📄 README.md                     # Этот файл
```
## 👥 Команда и роли
<div align="center">

<img src="https://github.com/mewkfeli.png" width="50" height="50" style="border-radius:50%">
  
mewkfeli	

ML-инженер / Backend	

• Разработка API для модели ИИ

• Интеграция трансформера

• Написание клиента для внешнего API

• Интеграция с ботом

<img src="https://github.com/eyeelwhy.png" width="50" height="50" style="border-radius:50%">

eyeelwhy	

Telegram Bot Developer	

• Разработка Telegram-бота

• Создание клавиатур и обработчиков

• Интеграция с API

</div>

