from telebot import types
from config import MAIN_CURRENCIES, CURRENCY_CODES


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("📝 Анализ текста"), types.KeyboardButton("🤖 GigaChat"))
    keyboard.row(types.KeyboardButton("💱 Конвертация"), types.KeyboardButton("📊 Курсы"))
    keyboard.row(types.KeyboardButton("💰 Список валют"), types.KeyboardButton("❓ Помощь"))
    keyboard.row(types.KeyboardButton("👋 Попрощаться"))
    return keyboard


def get_currency_selection_keyboard(action):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for code in CURRENCY_CODES[:5]:
        buttons.append(types.InlineKeyboardButton(
            f"{MAIN_CURRENCIES[code].split()[0]} {code}",
            callback_data=f"{action}_{code}"
        ))
    keyboard.row(*buttons)

    buttons = []
    for code in CURRENCY_CODES[5:]:
        buttons.append(types.InlineKeyboardButton(
            f"{MAIN_CURRENCIES[code].split()[0]} {code}",
            callback_data=f"{action}_{code}"
        ))
    keyboard.row(*buttons)

    keyboard.row(types.InlineKeyboardButton("❌ Отмена", callback_data="cancel"))
    return keyboard


def get_amount_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    amounts = [10, 50, 100, 500, 1000, 5000]
    buttons = []
    for amount in amounts:
        buttons.append(types.InlineKeyboardButton(f"{amount}", callback_data=f"amount_{amount}"))
    keyboard.add(*buttons)
    keyboard.row(types.InlineKeyboardButton("✏️ Своя сумма", callback_data="custom_amount"))
    keyboard.row(types.InlineKeyboardButton("◀️ Назад", callback_data="back_to_currencies"))
    keyboard.row(types.InlineKeyboardButton("❌ Отмена", callback_data="cancel"))
    return keyboard


def get_start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("/start"))
    return keyboard