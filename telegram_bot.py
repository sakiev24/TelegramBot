from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Функция, которая вызывается при команде /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который помогает узнать информацию о доступных медикаментах на кампусе.')

# Функция, которая вызывается при команде /medicines
def medicines(update: Update, context: CallbackContext) -> None:
    # Пример списка медикаментов
    medicines_list = [
        "Парацетамол - доступно 50 упаковок",
        "Ибупрофен - доступно 30 упаковок",
        "Антибиотик Амоксициллин - доступно 20 упаковок"
    ]
    reply_text = "\n".join(medicines_list)
    update.message.reply_text(reply_text)

def main() -> None:
    # Вставьте свой токен бота
    updater = Updater("")
    dispatcher = updater.dispatcher

    # Регистрируем обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("medicines", medicines))

    # Начинаем получать обновления от Telegram
    updater.start_polling()

    # Ожидаем сигнала завершения
    updater.idle()

if __name__ == '__main__':
    main()
