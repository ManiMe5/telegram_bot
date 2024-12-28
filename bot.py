import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Bot token
BOT_TOKEN = '7796485388:AAHthNhpzk15pex89pumf5UpDjrBIhDDCU8'

# Channel username (make sure the bot is added as an admin in this channel)
CHANNEL_USERNAME = '@myneey'

# Start the bot and display the menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Display menu options
    reply_markup = ReplyKeyboardMarkup(
        [['Send Music']], resize_keyboard=True
    )
    await update.message.reply_text(
        "Hello! Please choose one of the options below:", reply_markup=reply_markup
    )

# Send music to the channel
async def send_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Inform the user
    await update.message.reply_text("Please send your music file, and it will be posted to the channel.")
    return  # Wait for the user to upload a file

# Post the music file to the channel
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio or update.message.document or update.message.voice
    if file:
        # Inform the user about the upload
        await update.message.reply_text("Your file is being sent to the channel...")
        
        # Wait for 5 seconds before sending to the channel
        await asyncio.sleep(5)
        
        # Send the file to the channel
        if update.message.audio:
            await context.bot.send_audio(
                chat_id=CHANNEL_USERNAME,
                audio=file.file_id,
                caption="New music uploaded by the bot!"
            )
        elif update.message.document:
            await context.bot.send_document(
                chat_id=CHANNEL_USERNAME,
                document=file.file_id,
                caption="New file uploaded by the bot!"
            )
        elif update.message.voice:
            await context.bot.send_voice(
                chat_id=CHANNEL_USERNAME,
                voice=file.file_id,
                caption="New voice note uploaded by the bot!"
            )

        await update.message.reply_text("The file has been posted to the channel.")
    else:
        await update.message.reply_text("Please send a valid audio, document, or voice file.")

# Handle menu selection
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Send Music":
        await send_music(update, context)
    else:
        await update.message.reply_text("Please choose one of the menu options.")

# Main function to run the bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.ATTACHMENT, handle_file))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
