import requests
from telebot import types
import logging
from config import MAIN_CURRENCIES, CURRENCY_CODES
from keyboards import get_main_keyboard, get_currency_selection_keyboard, get_amount_keyboard, get_start_keyboard
from utils import format_gigachat_response, format_toxicity_response, validate_amount
from api_client import APIClient

# логирование модулей для отслеживания работы бота и отладки
logger = logging.getLogger(__name__)


def register_handlers(bot, user_states):
    @bot.message_handler(commands=['start'])
    def start(message):
        welcome_text = """
🌟 <b>Добро пожаловать в бота Ильи и Азалии!</b> 🌟

Бот создан в рамках проекта по предмету
Машинное обучение и Большие данные
Я помогу вам с тремя полезными сервисами:

📝 <b>Анализ тональности текста</b>
   - Определяю токсичность комментариев
   - Распознаю оскорбления, угрозы и мат

🤖 <b>GigaChat</b>
   - Отвечаю на любые вопросы
   - Помогаю с задачами

💱 <b>Валютный конвертер</b>
   - Конвертирую 10 популярных валют
   - Показываю актуальные курсы

<b>Используйте кнопки ниже для навигации!</b>
        """
        print(f"✅ Подключен новый пользователь!\nID: {message.chat.id}\nНикнейм: {message.from_user.username}")
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode='HTML')

    @bot.message_handler(commands=['help'])
    def help_command(message):
        help_text = """
📚 <b>Доступные команды и функции:</b>

📝 <b>Анализ текста:</b>
   • Нажмите кнопку "📝 Анализ текста"
   • Отправьте текст для анализа
   • Получите подробный разбор тональности

🤖 <b>GigaChat:</b>
   • Нажмите кнопку "🤖 GigaChat"
   • Задайте любой вопрос
   • Получите развернутый ответ

💱 <b>Конвертация валют:</b>
   • Нажмите кнопку "💱 Конвертация"
   • Выберите исходную валюту
   • Выберите целевую валюту
   • Выберите сумму (или введите свою)
   • Получите результат

📊 <b>Курсы валют:</b>
   • Нажмите кнопку "📊 Курсы"
   • Выберите валюту
   • Получите курсы к другим валютам

💰 <b>Список валют:</b>
   • Показывает все доступные валюты

👋 <b>Попрощаться:</b>
   • Завершить работу с ботом

<i>Выберите действие на клавиатуре ниже!</i>
        """
        bot.send_message(message.chat.id, help_text, reply_markup=get_main_keyboard(), parse_mode='HTML')

    @bot.message_handler(func=lambda message: message.text == "📝 Анализ текста")
    def handle_analyze_button(message):
        bot.send_message(
            message.chat.id,
            "📝 <b>Режим анализа текста</b>\n\nОтправьте текст, который нужно проанализировать:",
            reply_markup=get_main_keyboard(),
            parse_mode='HTML'
        )
        user_states[message.chat.id] = 'analyze'

    @bot.message_handler(func=lambda message: message.text == "🤖 GigaChat")
    def handle_gigachat_button(message):
        bot.send_message(
            message.chat.id,
            "🤖 <b>Режим GigaChat</b>\n\nЗадайте любой вопрос, и я постараюсь на него ответить:",
            reply_markup=get_main_keyboard(),
            parse_mode='HTML'
        )
        user_states[message.chat.id] = 'gigachat'

    @bot.message_handler(func=lambda message: message.text == "💱 Конвертация")
    def handle_convert_button(message):
        keyboard = get_currency_selection_keyboard('convert_from')
        bot.send_message(
            message.chat.id,
            "💱 <b>Конвертация валют</b>\n\nВыберите исходную валюту:",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
        user_states[message.chat.id] = 'select_from_currency'

    @bot.message_handler(func=lambda message: message.text == "📊 Курсы")
    def handle_rates_button(message):
        keyboard = get_currency_selection_keyboard('rates')
        bot.send_message(
            message.chat.id,
            "📊 <b>Курсы валют</b>\n\nВыберите валюту для просмотра курсов:",
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    @bot.message_handler(func=lambda message: message.text == "💰 Список валют")
    def handle_list_button(message):
        currencies_text = ""
        for code, name in MAIN_CURRENCIES.items():
            currencies_text += f"• <b>{code}</b> - {name}\n"

        reply = f"""
💰 <b>Доступные валюты:</b>

{currencies_text}

<i>Используйте эти коды для конвертации!</i>
        """
        bot.send_message(message.chat.id, reply, reply_markup=get_main_keyboard(), parse_mode='HTML')

    @bot.message_handler(func=lambda message: message.text == "❓ Помощь")
    def handle_help_button(message):
        help_command(message)

    @bot.message_handler(func=lambda message: message.text == "👋 Попрощаться")
    def handle_goodbye_button(message):
        goodbye_text = """
👋 <b>До свидания!</b>

Был рад помочь! Если захотите воспользоваться моими услугами снова, просто нажмите /start

Хорошего дня! 🌟
        """
        bot.send_message(message.chat.id, goodbye_text, parse_mode='HTML')
        bot.send_message(
            message.chat.id,
            "Чтобы начать заново, нажмите кнопку ниже:",
            reply_markup=get_start_keyboard()
        )
        print(f"Пользователь: {message.chat.id} - {message.from_user.username} отключился.")

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == "cancel":
            bot.edit_message_text(
                "❌ Действие отменено",
                chat_id,
                message_id,
                reply_markup=None
            )
            bot.send_message(chat_id, "Выберите действие:", reply_markup=get_main_keyboard())
            if chat_id in user_states:
                del user_states[chat_id]

        elif call.data == "back_to_currencies":
            keyboard = get_currency_selection_keyboard('convert_from')
            bot.edit_message_text(
                "💱 <b>Конвертация валют</b>\n\nВыберите исходную валюту:",
                chat_id,
                message_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            user_states[chat_id] = 'select_from_currency'

        elif call.data == "custom_amount":
            bot.edit_message_text(
                "💱 <b>Конвертация валют</b>\n\n"
                "✏️ Введите свою сумму (только число, например: 250 или 1500.50):",
                chat_id,
                message_id,
                reply_markup=None,
                parse_mode='HTML'
            )
            user_states[chat_id] = ('waiting_for_amount', user_states[chat_id][1], user_states[chat_id][2])

        elif call.data.startswith('convert_from_'):
            currency = call.data.replace('convert_from_', '')
            user_states[chat_id] = ('convert_from', currency)

            keyboard = get_currency_selection_keyboard('convert_to')
            bot.edit_message_text(
                f"💱 <b>Конвертация валют</b>\n\n"
                f"Исходная валюта: <b>{MAIN_CURRENCIES[currency]}</b>\n\n"
                f"Теперь выберите целевую валюту:",
                chat_id,
                message_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

        elif call.data.startswith('convert_to_'):
            to_currency = call.data.replace('convert_to_', '')
            from_currency = user_states[chat_id][1]
            user_states[chat_id] = ('convert_amount', from_currency, to_currency)

            keyboard = get_amount_keyboard()
            bot.edit_message_text(
                f"💱 <b>Конвертация валют</b>\n\n"
                f"🇺 <b>{MAIN_CURRENCIES[from_currency]}</b>\n"
                f"   ↓\n"
                f"🇺 <b>{MAIN_CURRENCIES[to_currency]}</b>\n\n"
                f"Выберите сумму для конвертации:",
                chat_id,
                message_id,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

        elif call.data.startswith('amount_'):
            amount = float(call.data.replace('amount_', ''))
            state_data = user_states[chat_id]
            from_currency = state_data[1]
            to_currency = state_data[2]

            bot.edit_message_text(
                f"💱 <b>Конвертация валют</b>\n\n"
                f"🔄 Конвертирую {amount} {from_currency} в {to_currency}...",
                chat_id,
                message_id,
                reply_markup=None,
                parse_mode='HTML'
            )

            perform_conversion(chat_id, from_currency, to_currency, amount)
            del user_states[chat_id]

        elif call.data.startswith('rates_'):
            currency = call.data.replace('rates_', '')

            bot.edit_message_text(
                f"📊 Получаю курсы для {currency}...",
                chat_id,
                message_id,
                reply_markup=None
            )

            try:
                result = APIClient.get_rates(currency)
                rates = result['rates']

                rates_text = ""
                for code in CURRENCY_CODES:
                    if code in rates and code != currency:
                        flag = MAIN_CURRENCIES[code].split()[0]
                        rates_text += f"{flag} <b>{code}</b>: {rates[code]:.4f}\n"

                reply = f"""
📊 <b>Курсы для {MAIN_CURRENCIES[currency]}</b>
📅 на {result['last_updated']}

{rates_text}

<i>Курсы обновляются ежедневно</i>
                """

                bot.send_message(chat_id, reply, reply_markup=get_main_keyboard(), parse_mode='HTML')

            except Exception as e:
                bot.send_message(
                    chat_id,
                    f"❌ Ошибка при получении курсов: {str(e)}",
                    reply_markup=get_main_keyboard()
                )

    def perform_conversion(chat_id, from_currency, to_currency, amount):
        try:
            result = APIClient.convert_currency(from_currency, to_currency, amount)

            reply = f"""
💱 <b>Результат конвертации</b>

{amount:,.2f} <b>{from_currency}</b> = 
💰 <b>{result['converted_amount']:,.2f} {to_currency}</b>

📊 Курс: 1 {from_currency} = {result['rate']:.4f} {to_currency}
🕐 Обновлено: {result['last_updated']}
            """

            bot.send_message(chat_id, reply, reply_markup=get_main_keyboard(), parse_mode='HTML')

        except Exception as e:
            bot.send_message(
                chat_id,
                f"❌ Ошибка при конвертации: {str(e)}",
                reply_markup=get_main_keyboard()
            )

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        chat_id = message.chat.id
        # Проверяем, есть ли у пользователя активное состояние (например, ожидание текста для анализа)
        if chat_id in user_states:
            state = user_states[chat_id]

            if state == 'analyze':
                bot.send_message(chat_id, f"🔍 <b>Анализирую текст...</b>", parse_mode='HTML')

                try:
                    # Отправляем текст на анализ через API-клиент
                    result = APIClient.analyze_comment(message.text)
                    result['text'] = message.text
                    # форматируем результат анализа в читаемый вид с эмодзи и отправляем юзеру
                    reply = format_toxicity_response(result)
                    bot.send_message(chat_id, reply, reply_markup=get_main_keyboard(), parse_mode='HTML')

                except requests.exceptions.ConnectionError:
                    bot.send_message(
                        chat_id,
                        "❌ Ошибка подключения к API. Убедитесь, что сервер запущен.",
                        reply_markup=get_main_keyboard()
                    )
                except Exception as e:
                    bot.send_message(
                        chat_id,
                        f"❌ Ошибка при анализе: {str(e)}",
                        reply_markup=get_main_keyboard()
                    )

                del user_states[chat_id]

            elif state == 'gigachat':
                bot.send_message(chat_id, f"🤔 <b>Отправляю запрос к GigaChat...</b>", parse_mode='HTML')

                try:
                    result = APIClient.gigachat_request(message.text)
                    formatted_response = format_gigachat_response(result['response'])

                    reply = f"""
🤖 <b>Ответ GigaChat:</b>

{formatted_response}
                    """

                    bot.send_message(chat_id, reply, reply_markup=get_main_keyboard(), parse_mode='HTML')

                except requests.exceptions.ConnectionError:
                    bot.send_message(
                        chat_id,
                        "❌ Ошибка подключения к API. Убедитесь, что сервер запущен.",
                        reply_markup=get_main_keyboard()
                    )
                except Exception as e:
                    bot.send_message(
                        chat_id,
                        f"❌ Ошибка при запросе к GigaChat: {str(e)}",
                        reply_markup=get_main_keyboard()
                    )

                del user_states[chat_id]

            elif isinstance(state, tuple) and state[0] == 'waiting_for_amount':
                amount = validate_amount(message.text)
                if amount:
                    from_currency = state[1]
                    to_currency = state[2]

                    bot.send_message(
                        chat_id,
                        f"💱 <b>Конвертация валют</b>\n\n"
                        f"🔄 Конвертирую {amount} {from_currency} в {to_currency}...",
                        parse_mode='HTML'
                    )

                    perform_conversion(chat_id, from_currency, to_currency, amount)
                    del user_states[chat_id]
                else:
                    bot.send_message(
                        chat_id,
                        "❌ Пожалуйста, введите корректное положительное число (например: 250 или 1500.50)",
                        reply_markup=get_main_keyboard()
                    )

            elif isinstance(state, tuple) and (state[0] == 'convert_from' or state[0] == 'convert_amount'):
                pass
            else:
                del user_states[chat_id]
                bot.send_message(
                    chat_id,
                    "Используйте кнопки меню для навигации",
                    reply_markup=get_main_keyboard()
                )
        else:
            bot.send_message(
                chat_id,
                "Используйте кнопки меню для выбора действия",
                reply_markup=get_main_keyboard()
            )