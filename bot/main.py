import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    filters, ContextTypes,
)
from sheets import append_submission, make_row
from validation import valid_phone, valid_email


# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SHEET_NAME = os.getenv("SHEET_NAME", "Business Leads")

# Conversation states
(
    ASK_BUSINESS_NAME,
    ASK_DIRECTOR,
    ASK_COMPANY,
    ASK_JOB_TITLE,
    ASK_PHONE,
    ASK_EMAIL,
    CONFIRM_SAVE,
) = range(7)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Welcome! Let's collect your business details step by step.\n\n"
        "First, what is the *Business Name*?",
        parse_mode="Markdown"
    )
    return ASK_BUSINESS_NAME

# Step 1 - Business name
async def business_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["business_name"] = update.message.text.strip()
    await update.message.reply_text("Who is the *Director* of the business?")
    return ASK_DIRECTOR

# Step 2 - Director
async def director(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["director"] = update.message.text.strip()
    await update.message.reply_text("Please enter the *Company Name*.")
    return ASK_COMPANY

# Step 3 - Company
async def company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["company_name"] = update.message.text.strip()
    await update.message.reply_text("What is your *Job Title*?")
    return ASK_JOB_TITLE

# Step 4 - Job Title
async def job_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["job_title"] = update.message.text.strip()
    await update.message.reply_text("📞 Please enter your *Phone Number*.")
    return ASK_PHONE

# Step 5 - Phone
async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not valid_phone(txt):
        await update.message.reply_text(
            "⚠️ That phone number looks invalid. Please enter a valid one (digits, +, spaces allowed)."
        )
        return ASK_PHONE
    context.user_data["phone"] = txt
    await update.message.reply_text("✉️ Please enter your *Email Address*.")
    return ASK_EMAIL

# Step 6 - Email
async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not valid_email(txt):
        await update.message.reply_text(
            "⚠️ That email looks invalid. Please try again (e.g. name@example.com)."
        )
        return ASK_EMAIL

    context.user_data["email"] = txt

    summary = (
        f"✅ Please confirm your details:\n\n"
        f"• Business Name: {context.user_data['business_name']}\n"
        f"• Director: {context.user_data['director']}\n"
        f"• Company Name: {context.user_data['company_name']}\n"
        f"• Job Title: {context.user_data['job_title']}\n"
        f"• Phone: {context.user_data['phone']}\n"
        f"• Email: {context.user_data['email']}\n\n"
        f"Type *save* to confirm or *cancel* to discard.",
    )
    await update.message.reply_text(summary, parse_mode="Markdown")
    return CONFIRM_SAVE

# Step 7 - Save or cancel
async def confirm_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip().lower()
    if txt == "save":
        tg_user = f"{update.effective_user.full_name} (@{update.effective_user.username})"
        row = make_row(context.user_data, tg_user)
        try:
            append_submission(SHEET_NAME, row)
            await update.message.reply_text(
                "✅ Your details have been saved to Google Sheets. Thank you!",
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as e:
            await update.message.reply_text(
                f"⚠️ Could not save to Google Sheets: {e}"
            )
        return ConversationHandler.END

    elif txt == "cancel":
        await update.message.reply_text(
            "❌ Submission canceled.", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    else:
        await update.message.reply_text("Please type 'save' or 'cancel'.")
        return CONFIRM_SAVE

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Conversation canceled.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Main application
def main():
    if not BOT_TOKEN:
        raise RuntimeError("⚠️ TELEGRAM_BOT_TOKEN missing in .env file")

    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_BUSINESS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, business_name)],
            ASK_DIRECTOR:      [MessageHandler(filters.TEXT & ~filters.COMMAND, director)],
            ASK_COMPANY:       [MessageHandler(filters.TEXT & ~filters.COMMAND, company)],
            ASK_JOB_TITLE:     [MessageHandler(filters.TEXT & ~filters.COMMAND, job_title)],
            ASK_PHONE:         [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            ASK_EMAIL:         [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            CONFIRM_SAVE:      [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_save)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("cancel", cancel))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
