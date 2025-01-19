from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
from datetime import time

# Советы от кошки
CAT_ADVICE = [
    "Иногда лучше просто полежать на солнце.",
    "Мурлыканье улучшает настроение.",
    "Не забудь потянуться утром, как это делают кошки.",
    "Никогда не бойся прыгать высоко.",
    "Сохраняй спокойствие, даже если всё вокруг бегает.",
    "Спи, когда хочется. Еда и сон — залог счастья."
]

# Функция для отправки совета от кошки
async def send_cat_advice(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    advice = random.choice(CAT_ADVICE)
    await context.bot.send_message(chat_id=chat_id, text=advice)

# Команда для старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой кошачий советник. Хочешь получать полезные советы каждый день? Отправь /subscribe, чтобы подписаться.")

# Команда для подписки
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Проверяем наличие job_queue
    if context.job_queue is None:
        await update.message.reply_text("Ошибка: JobQueue не активирован. Пожалуйста, свяжитесь с разработчиком.")
        return

    # Удаляем старую задачу, если она существует
    job_removed = context.job_queue.get_jobs_by_name(str(chat_id))
    for job in job_removed:
        job.schedule_removal()

    # Запускаем новую задачу в 7:00
    context.job_queue.run_daily(send_cat_advice, time=time(7, 0, 0), chat_id=chat_id, name=str(chat_id))

    # Отправляем подтверждение
    await update.message.reply_text("Ты успешно подписался на кошачьи советы! Сообщения будут приходить каждый день в 7:00.\n Начни день с кошачьей мудростью😽")

# Главная функция для запуска бота
def main():
    # Вставьте ваш токен от BotFather
    TOKEN = "7181024326:AAH0TorCvRP6uwOfx3RD5JVCNsUhGbEyTpo"

    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("subscribe", subscribe))

    # Запуск бота
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
