import os
import logging

# Third-party libraries
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from google import genai  # Required for the new Gemini SDK Client

# ==========================================
# ENVIRONMENT VARIABLES & CONFIGURATION
# ==========================================
# Load sensitive credentials from the local .env file securely
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_JawabAja_Bot")
TELEGRAM_DEVELOPER_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini Generative AI Client with the provided API Key
client = genai.Client(api_key=GOOGLE_API_KEY)

# ==========================================
# SYSTEM LOGGING SETUP
# ==========================================
# Configure basic logging to monitor bot activity, track routing, and capture errors in the terminal
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==========================================
# BOT COMMAND HANDLERS
# ==========================================
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the standard Telegram /start command.

    This asynchronous function serves as the primary entry point when a user first 
    interacts with the bot. It acts similarly to the initial landing page or 
    welcoming screen in a frontend framework like Streamlit.

    Args:
        update (telegram.Update): The payload containing incoming message details.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object to interact with the bot API.
    """
    
    # Safely extract the unique ID of the chat session to route the response
    chat_id = update.effective_chat.id
    
    # Construct the welcoming interface text
    welcome_text = (
        "🤖 **Hello! I am your AI Assistant.**\n\n"
        "I am powered by Google Gemini and ready to help. "
        "Send me a message to start chatting, brainstorm ideas, or ask any questions!"
    )

    # Transmit the message back to the user's Telegram client asynchronously
    await context.bot.send_message(
        chat_id=chat_id, 
        text=welcome_text,
        parse_mode='Markdown' # Enables bold text and basic formatting
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Processes standard text messages sent by the user to the bot.
    
    This handler acts as the core conversational engine. It captures the user's input, 
    forwards it to the Google Gemini LLM for processing, and seamlessly transmits 
    the generated response back to the Telegram chat.
    
    Args:
        update (telegram.Update): The payload containing incoming message details.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object for API interactions.
    """
    
    # 1. Extract metadata and user input from the incoming Telegram update
    user_text = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Initialize an empty string to store the final response
    reply_text = ""

    try:
        # 2. Inject the user's name into the prompt so the AI feels more personal
        # We tell the AI who is speaking before giving it the actual message
        contextual_prompt = f"The user you are talking to is named {user_name}. They said: '{user_text}'"

        # 3. Trigger the 'Typing...' action indicator in the Telegram UI
        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

        # 4. Invoke the Google Gemini Generative AI Model with the contextual prompt
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contextual_prompt,
        )

        # 5. Validate the LLM output safely
        if response.text and len(response.text.strip()) > 0:
            reply_text = response.text
        else:
            # Graceful fallback if the AI's mind goes blank
            reply_text = "I'm sorry, my AI engine couldn't process that. Could you try rephrasing?"
            
    except Exception as e: 
        # 6. Handle API failures securely and categorize the error
        error_msg = str(e).lower()
        logging.error(f"Failed to generate AI response for User {user_id} ({user_name}): {e}")
        
        # Check if the error is due to API quota limits or rate limiting
        if "quota" in error_msg or "429" in error_msg or "exhausted" in error_msg:
            reply_text = "⚠️ **API Limit Reached:** My AI engine is receiving too many requests right now or has reached its daily capacity. Please try again later or tomorrow!"
            
        # Check if the error is due to an invalid or missing API key
        elif "api_key" in error_msg or "key invalid" in error_msg:
            reply_text = "🛑 **Configuration Error:** My API key seems to be invalid or expired. Please report this to the Developer!"
        
        # Fallback for any other unexpected system errors (e.g., server down)
        else:
            reply_text = "⚠️ **System Error:** My AI engine is currently unreachable or busy. Please try again in a moment!"

    # 7. Transmit the final formulated text back to the user asynchronously
    await context.bot.send_message(
        chat_id=chat_id, 
        text=reply_text, 
        parse_mode="Markdown"
    )

# ==========================================
# GLOBAL ERROR HANDLING
# ==========================================
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global error handler for the Telegram bot routing system.
    
    This function acts as the ultimate safety net ("Ambulance"). If any handler 
    encounters an unhandled exception, it logs the error to the terminal and 
    sends a direct emergency message to the developer's Telegram chat.
    
    Args:
        update (telegram.Update): The incoming update that caused the error.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context containing the error object.
    """
    
    # 1. Log the critical error to the system console for debugging
    logging.error(f"Exception while handling an update: {context.error}")

    # 2. Construct the emergency notification payload
    error_message = (
        f"🚨 **SYSTEM ALERT: BOT ENCOUNTERED AN ERROR!** 🚨\n\n"
        f"**Error Details:**\n`{context.error}`"
    )

    # 3. Attempt to alert the developer via Telegram DM
    try:
        # We use TELEGRAM_DEVELOPER_CHAT_ID defined from our .env variables globally
        await context.bot.send_message(
            chat_id=TELEGRAM_DEVELOPER_CHAT_ID, 
            text=error_message, 
            parse_mode="Markdown"
        )
    except Exception as e:
        # If the bot fails to send the error message (e.g., developer blocked the bot), 
        # we log this failure and gracefully pass to prevent an infinite loop of crashes.
        logging.error(f"Failed to deliver error alert to Developer: {e}")
        pass

# ==========================================
# MAIN APPLICATION EXECUTOR
# ==========================================
if __name__ == "__main__":
    # 1. Initialize and build the Bot Application using the secure token
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # 2. Register standard Command Handlers (e.g., /start)
    app.add_handler(CommandHandler("start", start_command))
    
    # 3. Register standard Message Handlers 
    # Captures all regular text messages while ignoring commands.
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # 4. Register the Global Error Handler
    app.add_error_handler(error_handler)

    # 5. Ignite the engine and start continuous polling
    print("🚀 Gemini Q&A Telegram Bot is currently online and listening...")
    app.run_polling()