import re


def format_gigachat_response(text):
    """
    Форматирует ответ от GigaChat, убирая markdown разметку
    """
    if not text:
        return "❌ Пустой ответ от GigaChat"

    # Убираем ### в начале строк
    cleaned_text = re.sub(r'^###\s*', '', text, flags=re.MULTILINE)

    # Убираем ** (жирный текст)
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_text)

    # Убираем * (курсив) если есть
    cleaned_text = re.sub(r'\*(.*?)\*', r'\1', cleaned_text)

    return cleaned_text.strip()

def format_toxicity_response(result):
    tone_emojis = {
        'normal': '✅',
        'insult': '😡',
        'threat': '⚠️',
        'obscenity': '🔞'
    }

    tone_names = {
        'normal': 'НОРМАЛЬНО',
        'insult': 'ОСКОРБЛЕНИЕ',
        'threat': 'УГРОЗА',
        'obscenity': 'НЕНОРМАТИВНАЯ ЛЕКСИКА'
    }

    predictions_text = ""
    for label, value in result['predictions'].items():
        bar_length = int(value * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        predictions_text += f"{tone_emojis.get(label, '•')} {tone_names[label]}\n"
        predictions_text += f"   {bar} {value * 100:.1f}%\n\n"

    if result['is_toxic']:
        header = "🚨 ТОКСИЧНЫЙ КОММЕНТАРИЙ"
        border = "-" * 20
    else:
        header = "✅ БЕЗОПАСНЫЙ КОММЕНТАРИЙ"
        border = "-" * 20

    dominant_tone_emoji = tone_emojis.get(result['dominant_tone'], '📊')
    dominant_tone_name = tone_names.get(result['dominant_tone'], result['dominant_tone'])

    reply = f"""
{border}
{header}
{border}

{dominant_tone_emoji} Преобладающий тон: {dominant_tone_name}

📊 Детальный анализ:
{predictions_text}
🔍 Анализированный текст:
"_{result['text'][:100]}{'...' if len(result['text']) > 100 else ''}_"
    """
    return reply

def validate_amount(amount_text):
    amount_text = amount_text.strip().replace(',', '.')
    if re.match(r'^\d+\.?\d*$', amount_text):
        amount = float(amount_text)
        if amount > 0:
            return amount
    return None