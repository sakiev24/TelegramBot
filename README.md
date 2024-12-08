# UCA Medication Availability Telegram Bot
Here is the link to our [TelegramBot](https://t.me/MedicineUCA_Bot)
## Introduction
The UCA Medication Availability Telegram Bot project was developed to address a critical need among students at the University of Central Asia (UCA). While the university has a well-stocked cabinet of medications managed by Kiyal Eje, students often lack timely information about the availability of specific medicines. This project leverages Python and the Telegram Bot API to create a simple, efficient solution that provides real-time information about the medications available on campus.

The bot is designed to assist students during emergencies and routine health issues by offering easy access to the university's healthcare resources, ultimately contributing to a healthier campus environment.

## Problem Statement
Students living on campus often face health challenges and emergencies, necessitating quick access to medications. Despite the availability of a well-stocked medication cabinet, the lack of a transparent system for checking medication availability creates unnecessary delays and stress. This project addresses this issue by developing a Telegram bot that allows students to instantly check the availability of medications in Kiyal Eje's office, enhancing healthcare accessibility on campus.

## Objective and Solution
The primary objective is to develop a reliable and user-friendly Telegram bot to provide UCA students with real-time information about the availability of medications. The proposed solution involves:

* Bot Setup: Creating and deploying a Telegram bot.
* Database Creation: Storing and managing medication data.
* Bot Logic Development: Implementing commands and handlers to process user inquiries.
* User Interface Design: Providing an intuitive chat-based interface.
* Testing and Feedback: Ensuring functionality and gathering user input.
* Deployment: Hosting the bot on a cloud platform for continuous availability.

# Program Description
## Bot Features

* Medication Information:
    * Categorized access to medications.
    * Details about specific medications (e.g., uses, precautions).
* Emergency Contacts:
    * A predefined list of emergency contacts accessible via the bot.
    

## How It Works

* User Interaction:
    * The bot responds to user commands and messages through a structured menu.
    
* Medication Lookup:
    * Users can browse medication categories and retrieve information about specific drugs.
    
* Emergency Assistance:
    * A list of emergency contacts is provided to address urgent needs.

# Code Documentation
## Core Components

* Libraries Used
    * telebot: For creating and managing the Telegram bot.
    * telebot.types: For designing custom keyboards and inline buttons.
    
* Data Structures
    * Medications Dictionary: Stores categories and lists of medications
    ```
    medications = {
    "Pain Relief": ["Paracetamol", "Ibuprofen", "Citramon", "Aspirin"],
    "Antibiotics": ["Amoxicillin", "Ciprofloxacin", "Metronidazole (Flagyl)"],
    ...
    }
    ```
    * Emergency Contacts Dictionary: Stores names and phone numbers:
    ```
    emergency_contacts = {
    "Campus Doctor": "+996 708 136 013",
    "Ambulance": "103*",
    "Azat Baike": "+996 772 178 743"
    }
    ```
* Functions and Handlers
    * Markdown Escaping:

    Ensures special characters in text are escaped to avoid formatting issues:
    ```
    def escape_markdown(text):
    special_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_characters:
        text = text.replace(char, f"\\{char}")
    return text
    ```
    Start Command

    Initializes the bot and displays the main menu:
    ```
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
    ```
    Medication Categories

    Displays a list of categories and allows users to select a category:
    ```
    @bot.message_handler(func=lambda message: message.text == "💊 Medications")
    def show_categories(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    categories = list(medications.keys())
    for category in categories:
        callback_data = category.replace(" ", "_").lower()
        markup.add(types.InlineKeyboardButton(category, callback_data=f"category_{callback_data}"))
    bot.reply_to(message, "Select a medication category:", reply_markup=markup)
    ```
    Emergency Contacts

    Displays the list of emergency contacts:
    ```
    @bot.message_handler(func=lambda message: message.text.strip() == "🚨 Emergency Contacts")
    def show_emergency_contacts(message):
    response = "📞 *Emergency Contacts*\n"
    for name, contact in emergency_contacts.items():
        safe_contact = escape_markdown(contact)
        response += f"🔹 *{name}*: {safe_contact}\n"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")
    ```
    Callback Query Handlers

    Processes category and medication selections:
    ```
    @bot.callback_query_handler(func=lambda call: call.data.startswith("category_"))
    def handle_callback(call):
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
    ```
## Implementation Steps
* 1 Setup:
    * Create the bot using BotFather and obtain the API token.
* 2 Database:
    * Populate the dictionaries with relevant data.
* 3 Bot Development:
    * Implement handlers for user interactions.
* 4 Testing:
    * Test with sample queries to ensure proper functionality.
* 5 Deployment:
    * Host the bot on a cloud platform for continuous access.
# Conclusion
The UCA Medication Availability Telegram Bot addresses a critical gap in healthcare accessibility for students on campus. By leveraging Python and Telegram's API, the bot provides a fast and efficient way for students to check medication availability and access emergency contact information. This project not only simplifies healthcare access but also enhances the overall quality of life for UCA students. Through testing and feedback, the bot can be improved further to meet the evolving needs of the university community.
    
