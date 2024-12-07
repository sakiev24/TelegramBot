import telebot
from telebot import types

bot = telebot.TeleBot('8069347907:AAFi_TMVNLp0H1YbO1u0-pIvCxiLTd0Cm2w')  

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

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')

# /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'Use this bot to get information about medications. Start by choosing a category.')

# Show categories
@bot.message_handler(content_types=["text"])
def show_categories(message):
    markup = types.InlineKeyboardMarkup(row_width=2)  # Set row width to 2 buttons per row
    categories = list(medications.keys())

    for category in categories[:8]:  # Show the first 8 categories
        callback_data = category.replace(" ", "_").lower()  # Shorten callback data
        markup.add(types.InlineKeyboardButton(category, callback_data=f"category_{callback_data}"))

    # Add navigation if needed
    if len(categories) > 8:
        markup.add(types.InlineKeyboardButton("Next", callback_data="next_1"))

    bot.reply_to(message, "Select a medication category:", reply_markup=markup)

# Handle callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    print(f"Callback received: {call.data}")  # Debugging

    if call.data.startswith("category_"):
        category_key = call.data.split("_", 1)[1].replace("_", " ").title()  # Extract the category name
        meds = medications.get(category_key, [])
        markup = types.InlineKeyboardMarkup(row_width=1)  # One button per row

        for med in meds:
            callback_data = med.replace(" ", "_").lower()
            markup.add(types.InlineKeyboardButton(med, callback_data=f"med_{callback_data}"))

        bot.edit_message_text(f"Medications in {category_key}:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

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

    elif call.data.startswith("next_") or call.data.startswith("prev_"):
        page = int(call.data.split("_")[1])
        categories = list(medications.keys())
        start = page * 8
        end = start + 8
        markup = types.InlineKeyboardMarkup(row_width=2)

        for category in categories[start:end]:  # Show categories for this page
            callback_data = category.replace(" ", "_").lower()
            markup.add(types.InlineKeyboardButton(category, callback_data=f"category_{callback_data}"))

        # Add navigation buttons
        if start > 0:
            markup.add(types.InlineKeyboardButton("Previous", callback_data=f"prev_{page - 1}"))
        if end < len(categories):
            markup.add(types.InlineKeyboardButton("Next", callback_data=f"next_{page + 1}"))

        bot.edit_message_text("Select a medication category:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)

# Start the bot
bot.polling(none_stop=True)
