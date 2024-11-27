import os
import json
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
    MANAGE_URLS,
    ADD_NEW_URL,
    ADD_NEW_LABEL,
    EDIT_URL,
    EDIT_LABEL,
    INSERT_POST,
    URL_SELECTION,
    LABEL_SELECTION,
    WAITING_FOR_TEXT,
    WAITING_FOR_IMAGE,
    CONFIRM_POST,
    WAITING_FOR_URL_EDIT,
    WAITING_FOR_LABEL_EDIT,
) = range(15)

# Store admins and post data
admins = set()
post_data = {}

# File to store URLs and labels
URLS_FILE = "urls_and_labels.json"


def load_urls_and_labels():
    """Load URLs and labels from file"""
    try:
        with open(URLS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"urls": [], "labels": []}


def save_urls_and_labels(data):
    """Save URLs and labels to file"""
    with open(URLS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# Load existing URLs and labels
urls_and_labels = load_urls_and_labels()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler - shows main menu"""
    keyboard = [
        [InlineKeyboardButton("Add Admin", callback_data="add_admin")],
        [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
        [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Please select an option:", reply_markup=reply_markup
    )
    return MAIN_MENU


async def manage_urls_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show URL and label management menu"""
    keyboard = [
        [InlineKeyboardButton("Add New URL", callback_data="add_url")],
        [InlineKeyboardButton("Add New Label", callback_data="add_label")],
        [InlineKeyboardButton("View URLs", callback_data="view_urls")],
        [InlineKeyboardButton("View Labels", callback_data="view_labels")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="back_to_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "URL and Label Management"

    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return MANAGE_URLS


async def view_urls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display all URLs with edit/delete options"""
    keyboard = []
    for url in urls_and_labels["urls"]:
        keyboard.append(
            [
                InlineKeyboardButton(f"📝 {url}", callback_data=f"edit_url:{url}"),
                InlineKeyboardButton("❌", callback_data=f"delete_url:{url}"),
            ]
        )
    keyboard.append([InlineKeyboardButton("Back", callback_data="manage_urls")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "URLs (click to edit, ❌ to delete):"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return MANAGE_URLS


async def view_labels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display all labels with edit/delete options"""
    keyboard = []
    for label in urls_and_labels["labels"]:
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📝 {label}", callback_data=f"edit_label:{label}"
                ),
                InlineKeyboardButton("❌", callback_data=f"delete_label:{label}"),
            ]
        )
    keyboard.append([InlineKeyboardButton("Back", callback_data="manage_urls")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Labels (click to edit, ❌ to delete):"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return MANAGE_URLS


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses"""
    query = update.callback_query
    await query.answer()

    if query.data == "add_admin":
        if str(query.from_user.id) == os.getenv("OWNER_ID"):
            await query.message.edit_text(
                "Please forward a message from the user you want to add as admin."
            )
            return ADD_ADMIN
        else:
            await query.message.edit_text("Only the owner can add admins.")
            return ConversationHandler.END

    elif query.data == "manage_urls":
        if str(query.from_user.id) in admins or str(query.from_user.id) == os.getenv(
            "OWNER_ID"
        ):
            return await manage_urls_menu(update, context)
        else:
            await query.message.edit_text("Only admins can manage URLs and labels.")
            return ConversationHandler.END

    elif query.data == "view_urls":
        return await view_urls(update, context)

    elif query.data == "view_labels":
        return await view_labels(update, context)

    elif query.data.startswith("edit_url:"):
        url = query.data.replace("edit_url:", "")
        context.user_data["editing_url"] = url
        await query.message.edit_text(f"Please enter new URL to replace:\n{url}")
        return WAITING_FOR_URL_EDIT

    elif query.data.startswith("edit_label:"):
        label = query.data.replace("edit_label:", "")
        context.user_data["editing_label"] = label
        await query.message.edit_text(f"Please enter new label to replace:\n{label}")
        return WAITING_FOR_LABEL_EDIT

    elif query.data.startswith("delete_url:"):
        url = query.data.replace("delete_url:", "")
        urls_and_labels["urls"].remove(url)
        save_urls_and_labels(urls_and_labels)
        return await view_urls(update, context)

    elif query.data.startswith("delete_label:"):
        label = query.data.replace("delete_label:", "")
        urls_and_labels["labels"].remove(label)
        save_urls_and_labels(urls_and_labels)
        return await view_labels(update, context)

    elif query.data == "add_url":
        await query.message.edit_text("Please enter the new URL:")
        return ADD_NEW_URL

    elif query.data == "add_label":
        await query.message.edit_text("Please enter the new label:")
        return ADD_NEW_LABEL

    elif query.data == "back_to_main":
        keyboard = [
            [InlineKeyboardButton("Add Admin", callback_data="add_admin")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text("Main Menu:", reply_markup=reply_markup)
        return MAIN_MENU

    elif query.data == "insert_post":
        if str(query.from_user.id) in admins or str(query.from_user.id) == os.getenv(
            "OWNER_ID"
        ):
            context.user_data["post_data"] = {}
            # Show URL selection buttons
            keyboard = []
            for url in urls_and_labels["urls"]:
                keyboard.append([InlineKeyboardButton(url, callback_data=f"url:{url}")])
            keyboard.append(
                [InlineKeyboardButton("Add New URL", callback_data="new_url")]
            )
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.edit_text(
                "Select a URL or add a new one:", reply_markup=reply_markup
            )
            return URL_SELECTION
        else:
            await query.message.edit_text("Only admins can create posts.")
            return ConversationHandler.END

    elif query.data.startswith("url:"):
        url = query.data.replace("url:", "")
        context.user_data["post_data"]["url"] = url
        # Show label selection buttons
        keyboard = []
        for label in urls_and_labels["labels"]:
            keyboard.append(
                [InlineKeyboardButton(label, callback_data=f"label:{label}")]
            )
        keyboard.append(
            [InlineKeyboardButton("Add New Label", callback_data="new_label")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "Select a label or add a new one:", reply_markup=reply_markup
        )
        return LABEL_SELECTION

    elif query.data.startswith("label:"):
        label = query.data.replace("label:", "")
        context.user_data["post_data"]["label"] = label
        await query.message.edit_text("Please enter the post text:")
        return WAITING_FOR_TEXT

    elif query.data == "new_url":
        await query.message.edit_text("Please enter the new URL:")
        context.user_data["adding_new"] = "url"
        return ADD_NEW_URL

    elif query.data == "new_label":
        await query.message.edit_text("Please enter the new label:")
        context.user_data["adding_new"] = "label"
        return ADD_NEW_LABEL

    elif query.data == "confirm_post":
        # Send post to channel
        post_data = context.user_data.get("post_data", {})
        channel_id = os.getenv("CHANNEL_ID")

        keyboard = [
            [
                InlineKeyboardButton(
                    text=post_data.get("label", "Visit Website"),
                    url=post_data.get("url", ""),
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

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


async def handle_new_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new URL input"""
    new_url = update.message.text
    if "adding_new" in context.user_data:
        # Adding URL during post creation
        context.user_data["post_data"]["url"] = new_url
        urls_and_labels["urls"].append(new_url)
        save_urls_and_labels(urls_and_labels)
        # Show label selection
        keyboard = []
        for label in urls_and_labels["labels"]:
            keyboard.append(
                [InlineKeyboardButton(label, callback_data=f"label:{label}")]
            )
        keyboard.append(
            [InlineKeyboardButton("Add New Label", callback_data="new_label")]
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Select a label or add a new one:", reply_markup=reply_markup
        )
        return LABEL_SELECTION
    else:
        # Adding URL from management menu
        urls_and_labels["urls"].append(new_url)
        save_urls_and_labels(urls_and_labels)
        await update.message.reply_text(f"URL added: {new_url}")
        return await manage_urls_menu(update, context)


async def handle_new_label(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new label input"""
    new_label = update.message.text
    if "adding_new" in context.user_data:
        # Adding label during post creation
        context.user_data["post_data"]["label"] = new_label
        urls_and_labels["labels"].append(new_label)
        save_urls_and_labels(urls_and_labels)
        await update.message.reply_text("Please enter the post text:")
        return WAITING_FOR_TEXT
    else:
        # Adding label from management menu
        urls_and_labels["labels"].append(new_label)
        save_urls_and_labels(urls_and_labels)
        await update.message.reply_text(f"Label added: {new_label}")
        return await manage_urls_menu(update, context)


async def handle_url_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle URL editing"""
    new_url = update.message.text
    old_url = context.user_data["editing_url"]
    idx = urls_and_labels["urls"].index(old_url)
    urls_and_labels["urls"][idx] = new_url
    save_urls_and_labels(urls_and_labels)
    await update.message.reply_text(f"URL updated from:\n{old_url}\nto:\n{new_url}")
    return await view_urls(update, context)


async def handle_label_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle label editing"""
    new_label = update.message.text
    old_label = context.user_data["editing_label"]
    idx = urls_and_labels["labels"].index(old_label)
    urls_and_labels["labels"][idx] = new_label
    save_urls_and_labels(urls_and_labels)
    await update.message.reply_text(
        f"Label updated from:\n{old_label}\nto:\n{new_label}"
    )
    return await view_labels(update, context)


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
            MANAGE_URLS: [CallbackQueryHandler(button_handler)],
            ADD_NEW_URL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_url)
            ],
            ADD_NEW_LABEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_label)
            ],
            WAITING_FOR_URL_EDIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_edit)
            ],
            WAITING_FOR_LABEL_EDIT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_label_edit)
            ],
            URL_SELECTION: [CallbackQueryHandler(button_handler)],
            LABEL_SELECTION: [CallbackQueryHandler(button_handler)],
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
