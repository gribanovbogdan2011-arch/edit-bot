import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler,
    MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PRODUCT_PAYLOAD = "edit_access_100_stars"
PRODUCT_TITLE = "EDIT"
PRODUCT_DESCRIPTION = "Покупка цифрового товара EDIT"
SUPPORT_CONTACT = "@Gggjcfhbdtj"
DELIVERY_TEXT = "Ваш EDIT: @Gggjcfhbdtj"

if not BOT_TOKEN:
    raise RuntimeError("Переменная BOT_TOKEN не задана. Укажи токен локально в Termux.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Купить EDIT — 100 ⭐", callback_data="buy_edit")]]
    await update.message.reply_text(
        "Привет! Это EDIT — цифровой товар / доступ.\n"
        "Цена: 100 Telegram Stars.\n\n"
        "Нажми кнопку ниже, чтобы оплатить:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def buy_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=PRODUCT_TITLE,
        description=PRODUCT_DESCRIPTION,
        payload=PRODUCT_PAYLOAD,
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice("EDIT", 100)],
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.pre_checkout_query
    if q.invoice_payload != PRODUCT_PAYLOAD or q.currency != "XTR" or q.total_amount != 100:
        await q.answer(ok=False, error_message="Не удалось проверить заказ. Попробуйте ещё раз.")
        return
    await q.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    if (payment.invoice_payload == PRODUCT_PAYLOAD
            and payment.currency == "XTR"
            and payment.total_amount == 100):
        await update.message.reply_text("Оплата получена! Спасибо ❤️\n\n" + DELIVERY_TEXT)

async def paysupport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Если возник вопрос по оплате или заказу, напиши в поддержку: " + SUPPORT_CONTACT
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paysupport", paysupport))
    app.add_handler(CallbackQueryHandler(buy_edit, pattern="^buy_edit$"))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("EDIT BOT запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
