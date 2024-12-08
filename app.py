import telebot
from telebot import types

bot = telebot.TeleBot('7724630580:AAEZZ9jOqzVCcvfRdflZa5h4iTx8KpvaEYs')

# Medication categories
medications = {
    "Pain Relief": ["Paracetamol", "Ibuprofen", "Citramon", "Aspirin"],
    "Antibiotics": ["Amoxicillin", "Ciprofloxacin", "Metronidazole (Flagyl)"],
    "Antihistamines (Allergy Treatment)": ["Cetirizine", "Loratadine"],
    "Gastrointestinal Medications": ["Omeprazole", "Loperamide (Imodium)", "Activated Charcoal"],
    "Cardiovascular Emergencies": ["Nitroglycerin", "Amlodipine"],
    "Muscle Spasms": ["Noshpa"],
    "Respiratory Medications": ["Salbutamol (Ventolin)"],
    "Cold & Flu": ["TylolHot"],
    "First Aid and Wound Care": ["Hydrogen Peroxide", "Antiseptic Solution (Chlorhexidine)"]
}

# Emergency contacts
emergency_contacts = {
    "Campus Doctor": "+996 708 136 013",
    "Ambulance": "103*",
    "Azat Baike": "+996 772 178 743"
}

# Function to escape special Markdown characters
def escape_markdown(text):
    """Escape special characters for Markdown."""
    special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_characters:
        text = text.replace(char, f"\\{char}")
    return text

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_medications = types.KeyboardButton("💊 Medications")
    btn_emergency = types.KeyboardButton("🚨 Emergency Contacts")
    markup.add(btn_medications, btn_emergency)
    bot.send_message(
        message.chat.id,
        f'Hello, {message.from_user.first_name}! How can I assist you today?',
        reply_markup=markup
    )

# Handle "Medications" option
@bot.message_handler(func=lambda message: message.text == "💊 Medications")
def show_categories(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = list(medications.keys())

    for category in categories:
        callback_data = category.replace(" ", "_").lower()
        markup.add(types.InlineKeyboardButton(category, callback_data=f"category_{callback_data}"))

    bot.reply_to(message, "Select a medication category:", reply_markup=markup)

# Handle "Emergency Contacts" option
@bot.message_handler(func=lambda message: message.text.strip() == "🚨 Emergency Contacts")
def show_emergency_contacts(message):
    response = "📞 *Emergency Contacts*\n"
    for name, contact in emergency_contacts.items():
        safe_contact = escape_markdown(contact)  # Escape special characters
        response += f"🔹 *{name}*: {safe_contact}\n"

    try:
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    except Exception as e:
        print(f"Error sending message: {e}")

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith("category_"):
        category_key = call.data.split("_", 1)[1].replace("_", " ").title()
        meds = medications.get(category_key, [])
        markup = types.InlineKeyboardMarkup(row_width=1)

        for med in meds:
            callback_data = med.replace(" ", "_").lower()
            markup.add(types.InlineKeyboardButton(med, callback_data=f"med_{callback_data}"))

        bot.edit_message_text(
            f"Medications in {category_key}:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )


    elif call.data.startswith("med_"):
        med_name = call.data.split("_", 1)[1].replace("_", " ").title()
        details = {
            "Paracetamol": "Paracetamol is used for pain relief and fever.",
            "Ibuprofen": "Ibuprofen is used for pain, inflammation, and fever.",
            "Noshpa": "Noshpa is used to relieve pain from muscle spasms.",
            "Amoxicillin": "Amoxicillin is an antibiotic used for bacterial infections.",
            "Citramon": "Citramon is used for pain, headache, and fever.",
            "TylolHot": "TylolHot is used for cold and flu symptoms.",
            "Aspirin": "Aspirin is for pain relief and as a blood thinner.",
            "Ciprofloxacin": "For bacterial infections like urinary tract infections.",
            "Metronidazole (Flagyl)": "For bacterial and parasitic infections.",
            "Cetirizine": "For allergies and hay fever.",
            "Loratadine": "For seasonal allergies.",
            "Omeprazole": "For stomach ulcers and acid reflux.",
            "Loperamide (Imodium)": "For diarrhea control.",
            "Activated Charcoal": "For poisoning and indigestion.",
            "Nitroglycerin": "For chest pain or angina.",
            "Amlodipine": "For high blood pressure.",
            "Salbutamol (Ventolin)": "For asthma attacks.",
            "Hydrogen Peroxide": "For wound cleaning and disinfection.",
            "Antiseptic Solution (Chlorhexidine)": "For cleaning wounds."
        }
        response = details.get(med_name, "No information available for this medication.")
        bot.send_message(call.message.chat.id, response)

# Start the bot
bot.polling(none_stop=True)
