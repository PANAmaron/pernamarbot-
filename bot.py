import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
JOIN, WALLET = range(2)

# Replace these with your actual social links
TELEGRAM_CHANNEL = "https://t.me/your_channel"
TWITTER_PROFILE = "https://twitter.com/your_profile"

async def start(update: Update, context) -> int:
    """Initiate the airdrop process"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n"
        "🔥 Welcome to our exclusive SOLANA airdrop!\n\n"
        f"📢 Join our Telegram Channel: {TELEGRAM_CHANNEL}\n"
        f"🐦 Follow us on Twitter: {TWITTER_PROFILE}\n\n"
        "✅ Type /done when you've completed the steps"
    )
    return JOIN

async def done(update: Update, context) -> int:
    """After user claims they joined"""
    await update.message.reply_text(
        "🎉 Great! Now send your Solana wallet address to claim 10 SOL\n"
        "Example: 7sP5ab... or Ffhdsl..."
    )
    return WALLET

async def wallet(update: Update, context) -> int:
    """Handle wallet submission"""
    wallet_address = update.message.text
    logger.info(f"User submitted wallet: {wallet_address}")
    
    await update.message.reply_text(
        "🚀 CONGRATULATIONS!\n\n"
        "✅ You've successfully claimed 10 SOL!\n"
        f"💳 Wallet: {wallet_address}\n\n"
        "⚠️ Note: This is a test airdrop. No real tokens will be sent."
    )
    return ConversationHandler.END

async def cancel(update: Update, context) -> int:
    """Cancel the conversation"""
    await update.message.reply_text('❌ Airdrop canceled')
    return ConversationHandler.END

def main() -> None:
    """Run the bot"""
    # YOUR BOT TOKEN INSERTED HERE
    application = Application.builder().token("7583954766:AAFV6EqdH1V18v_tOnajiy42_mFU3fOPs38").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            JOIN: [CommandHandler('done', done)],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
