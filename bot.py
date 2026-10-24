import os
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

GIFTS = [
    "Flipkart Gift Card",
    "Flipkart ₹500",
    "Amazon",
    "Xbox Gift Card",
    "Myntra"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    buttons = []

    for g in GIFTS:
        buttons.append([
            InlineKeyboardButton(
                g,
                callback_data=f"gift|{g}"
            )
        ])

    await update.message.reply_text(
        "🎁 Microsoft Rewards",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def buttons(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("gift|"):

        name = data.split("|")[1]

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔔 Alert Me",
                    callback_data=f"alert|{name}"
                )
            ]
        ]

        await query.edit_message_text(
            f"🎁 {name}\n\n"
            "Status: Checking..."
            "\nPoints: Unknown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("alert|"):

        name = data.split("|")[1]

        await query.answer(
            f"Alerts enabled for {name}",
            show_alert=True
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
