import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# States for conversation handler
(
    MAIN_MENU,
    ADD_ADMIN,
    INSERT_POST,
    WAITING_FOR_URL,
    WAITING_FOR_LABEL,
    WAITING_FOR_TEXT,
    WAITING_FOR_IMAGE,
    CONFIRM_POST,
) = range(8)

# Store admins and post data
admins = set()
post_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler - shows main menu"""
    keyboard = [
        [InlineKeyboardButton("Add Admin", callback_data="add_admin")],
        [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Please select an option:", reply_markup=reply_markup
    )
    return MAIN_MENU


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()

    if query.data == "add_admin":
        # Check if user is owner
        if str(query.from_user.id) == os.getenv("OWNER_ID"):
            await query.message.edit_text(
                "Please forward a message from the user you want to add as admin."
            )
            return ADD_ADMIN
        else:
            await query.message.edit_text("Only the owner can add admins.")
            return ConversationHandler.END

    elif query.data == "insert_post":
        # Check if user is admin or owner
        if str(query.from_user.id) in admins or str(query.from_user.id) == os.getenv(
            "OWNER_ID"
        ):
            context.user_data["post_data"] = {}
            await query.message.edit_text("Please enter the web app URL:")
            return WAITING_FOR_URL
        else:
            await query.message.edit_text("Only admins can create posts.")
            return ConversationHandler.END

    elif query.data == "confirm_post":
        # Send post to channel
        post_data = context.user_data.get("post_data", {})
        channel_id = os.getenv("CHANNEL_ID")

        # Create inline keyboard with web app button
        keyboard = [
            [
                InlineKeyboardButton(
                    text=post_data.get("label", "Visit Website"),
                    url=post_data.get("url", ""),
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send image with caption and button
        await context.bot.send_photo(
            chat_id=channel_id,
            photo=post_data.get("image"),
            caption=post_data.get("text"),
            reply_markup=reply_markup,
        )

        await query.message.edit_text("Post has been sent to the channel!")
        return ConversationHandler.END

    elif query.data == "cancel_post":
        await query.message.edit_text("Post cancelled.")
        return ConversationHandler.END


async def handle_admin_forward(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle forwarded message for adding admin"""
    if update.message.forward_from:
        new_admin_id = str(update.message.forward_from.id)
        admins.add(new_admin_id)
        await update.message.reply_text(f"Admin added successfully!")
    else:
        await update.message.reply_text("Please forward a message from the user.")
    return ConversationHandler.END


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle web app URL input"""
    context.user_data["post_data"]["url"] = update.message.text
    await update.message.reply_text("Please enter the button label text:")
    return WAITING_FOR_LABEL


async def handle_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button label input"""
    context.user_data["post_data"]["label"] = update.message.text
    await update.message.reply_text("Please enter the post text:")
    return WAITING_FOR_TEXT


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle post text input"""
    context.user_data["post_data"]["text"] = update.message.text
    await update.message.reply_text("Please send the image for the post:")
    return WAITING_FOR_IMAGE


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image input"""
    if update.message.photo:
        context.user_data["post_data"]["image"] = update.message.photo[-1].file_id

        # Show preview and confirmation buttons
        post_data = context.user_data["post_data"]
        preview_text = f"Preview:\n\nURL: {post_data['url']}\nLabel: {post_data['label']}\nText: {post_data['text']}"

        keyboard = [
            [InlineKeyboardButton("Confirm & Send", callback_data="confirm_post")],
            [InlineKeyboardButton("Cancel", callback_data="cancel_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(preview_text, reply_markup=reply_markup)
        return CONFIRM_POST
    else:
        await update.message.reply_text("Please send an image file.")
        return WAITING_FOR_IMAGE


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(button_handler)],
            ADD_ADMIN: [MessageHandler(filters.ALL, handle_admin_forward)],
            WAITING_FOR_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)
            ],
            WAITING_FOR_LABEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_label)
            ],
            WAITING_FOR_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
            ],
            WAITING_FOR_IMAGE: [MessageHandler(filters.PHOTO, handle_image)],
            CONFIRM_POST: [CallbackQueryHandler(button_handler)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
