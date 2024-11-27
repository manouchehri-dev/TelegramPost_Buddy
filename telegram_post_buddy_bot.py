import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
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
    ADMIN_MENU,
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
    WAITING_FOR_ADMIN_ID,
) = range(17)

# Store admins and post data
ADMINS_FILE = "admins.json"


def load_admins():
    """Load admins from file"""
    try:
        with open(ADMINS_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_admins(admins):
    """Save admins to file"""
    with open(ADMINS_FILE, "w") as f:
        json.dump(list(admins), f)


admins = load_admins()
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
        [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
        [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
        [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Please select an option:", reply_markup=reply_markup
    )
    return MAIN_MENU


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin management menu"""
    keyboard = [
        [InlineKeyboardButton("Add Admin", callback_data="add_admin")],
        [InlineKeyboardButton("View/Remove Admins", callback_data="view_admins")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="back_to_main")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Admin Management"

    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return ADMIN_MENU


async def view_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display all admins with remove option"""
    keyboard = []
    for admin_id in admins:
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"Admin: {admin_id}", callback_data=f"admin_info:{admin_id}"
                ),
                InlineKeyboardButton("❌", callback_data=f"remove_admin:{admin_id}"),
            ]
        )
    keyboard.append([InlineKeyboardButton("Back", callback_data="manage_admins")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "Current Admins (❌ to remove):"
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)
    return ADMIN_MENU


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

    if query.data == "manage_admins":
        if str(query.from_user.id) == os.getenv("OWNER_ID"):
            return await admin_menu(update, context)
        else:
            await query.message.edit_text("Only the owner can manage admins.")
            return ConversationHandler.END

    elif query.data == "view_admins":
        return await view_admins(update, context)

    elif query.data.startswith("remove_admin:"):
        if str(query.from_user.id) == os.getenv("OWNER_ID"):
            admin_id = query.data.replace("remove_admin:", "")
            admins.remove(admin_id)
            save_admins(admins)
            return await view_admins(update, context)
        else:
            await query.message.edit_text("Only the owner can remove admins.")
            return ConversationHandler.END

    elif query.data == "add_admin":
        if str(query.from_user.id) == os.getenv("OWNER_ID"):
            await query.message.edit_text(
                "Please enter the Telegram ID of the user you want to add as admin:"
            )
            return WAITING_FOR_ADMIN_ID
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
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
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
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "Back to Main Menu", callback_data="back_to_main"
                    )
                ]
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
        keyboard.append([InlineKeyboardButton("Back", callback_data="insert_post")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "Select a label or add a new one:", reply_markup=reply_markup
        )
        return LABEL_SELECTION

    elif query.data.startswith("label:"):
        label = query.data.replace("label:", "")
        context.user_data["post_data"]["label"] = label
        keyboard = [
            [InlineKeyboardButton("Add Text", callback_data="add_text")],
            [InlineKeyboardButton("Skip Text", callback_data="skip_text")],
            [InlineKeyboardButton("Back", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "Would you like to add text to your post?", reply_markup=reply_markup
        )
        return WAITING_FOR_TEXT

    elif query.data == "add_text":
        await query.message.edit_text(
            "Please enter the post text:\n\n(Send /cancel to go back to main menu)"
        )
        context.user_data["post_data"]["adding_text"] = True
        return WAITING_FOR_TEXT

    elif query.data == "skip_text":
        context.user_data["post_data"]["text"] = ""  # Empty text
        keyboard = [
            [InlineKeyboardButton("Add Image", callback_data="add_image")],
            [InlineKeyboardButton("Skip Image", callback_data="skip_image")],
            [InlineKeyboardButton("Back", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "Would you like to add an image to your post?", reply_markup=reply_markup
        )
        return WAITING_FOR_IMAGE

    elif query.data == "add_image":
        await query.message.edit_text(
            "Please send the image for the post:\n\n(Send /cancel to go back to main menu)"
        )
        context.user_data["post_data"]["adding_image"] = True
        return WAITING_FOR_IMAGE

    elif query.data == "skip_image":
        post_data = context.user_data.get("post_data", {})
        preview_text = (
            f"Preview:\n\nURL: {post_data['url']}\nLabel: {post_data['label']}"
        )
        if post_data.get("text"):
            preview_text += f"\nText: {post_data['text']}"

        keyboard = [
            [InlineKeyboardButton("Confirm & Send", callback_data="confirm_post")],
            [InlineKeyboardButton("Cancel", callback_data="cancel_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(preview_text, reply_markup=reply_markup)
        return CONFIRM_POST

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

        if post_data.get("image"):
            # Send with image
            await context.bot.send_photo(
                chat_id=channel_id,
                photo=post_data.get("image"),
                caption=post_data.get("text", ""),
                reply_markup=reply_markup,
            )
        else:
            # Send text only
            await context.bot.send_message(
                chat_id=channel_id,
                text=post_data.get("text", ""),
                reply_markup=reply_markup,
            )

        await query.message.edit_text("Post has been sent to the channel!")
        return ConversationHandler.END

    elif query.data == "cancel_post":
        await query.message.edit_text("Post cancelled.")
        return ConversationHandler.END


async def handle_admin_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin ID input"""
    try:
        new_admin_id = str(update.message.text).strip()
        if new_admin_id.isdigit():
            admins.add(new_admin_id)
            save_admins(admins)
            await update.message.reply_text(
                f"Admin with ID {new_admin_id} added successfully!"
            )
            return await admin_menu(update, context)
        else:
            await update.message.reply_text("Please enter a valid numeric Telegram ID.")
            return WAITING_FOR_ADMIN_ID
    except Exception as e:
        await update.message.reply_text("Error adding admin. Please try again.")
        return WAITING_FOR_ADMIN_ID


async def handle_new_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new URL input"""
    if update.message.text == "/cancel":
        keyboard = [
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Operation cancelled. Back to main menu:", reply_markup=reply_markup
        )
        return MAIN_MENU

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
        keyboard.append([InlineKeyboardButton("Back", callback_data="insert_post")])
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
    if update.message.text == "/cancel":
        keyboard = [
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Operation cancelled. Back to main menu:", reply_markup=reply_markup
        )
        return MAIN_MENU

    new_label = update.message.text
    if "adding_new" in context.user_data:
        # Adding label during post creation
        context.user_data["post_data"]["label"] = new_label
        urls_and_labels["labels"].append(new_label)
        save_urls_and_labels(urls_and_labels)
        keyboard = [
            [InlineKeyboardButton("Add Text", callback_data="add_text")],
            [InlineKeyboardButton("Skip Text", callback_data="skip_text")],
            [InlineKeyboardButton("Back", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Would you like to add text to your post?", reply_markup=reply_markup
        )
        return WAITING_FOR_TEXT
    else:
        # Adding label from management menu
        urls_and_labels["labels"].append(new_label)
        save_urls_and_labels(urls_and_labels)
        await update.message.reply_text(f"Label added: {new_label}")
        return await manage_urls_menu(update, context)


async def handle_url_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle URL editing"""
    if update.message.text == "/cancel":
        keyboard = [
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Operation cancelled. Back to main menu:", reply_markup=reply_markup
        )
        return MAIN_MENU

    new_url = update.message.text
    old_url = context.user_data["editing_url"]
    idx = urls_and_labels["urls"].index(old_url)
    urls_and_labels["urls"][idx] = new_url
    save_urls_and_labels(urls_and_labels)
    await update.message.reply_text(f"URL updated from:\n{old_url}\nto:\n{new_url}")
    return await view_urls(update, context)


async def handle_label_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle label editing"""
    if update.message.text == "/cancel":
        keyboard = [
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Operation cancelled. Back to main menu:", reply_markup=reply_markup
        )
        return MAIN_MENU

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
    if update.message.text == "/cancel":
        keyboard = [
            [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
            [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
            [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Operation cancelled. Back to main menu:", reply_markup=reply_markup
        )
        return MAIN_MENU

    context.user_data["post_data"]["text"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Add Image", callback_data="add_image")],
        [InlineKeyboardButton("Skip Image", callback_data="skip_image")],
        [InlineKeyboardButton("Back", callback_data="insert_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Would you like to add an image to your post?", reply_markup=reply_markup
    )
    return WAITING_FOR_IMAGE


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle image input"""
    if update.message.photo:
        context.user_data["post_data"]["image"] = update.message.photo[-1].file_id

        # Show preview and confirmation buttons
        post_data = context.user_data["post_data"]
        preview_text = (
            f"Preview:\n\nURL: {post_data['url']}\nLabel: {post_data['label']}"
        )
        if post_data.get("text"):
            preview_text += f"\nText: {post_data['text']}"

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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current operation and return to main menu"""
    keyboard = [
        [InlineKeyboardButton("Manage Admins", callback_data="manage_admins")],
        [InlineKeyboardButton("Manage URLs & Labels", callback_data="manage_urls")],
        [InlineKeyboardButton("Insert Post", callback_data="insert_post")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Operation cancelled. Back to main menu:", reply_markup=reply_markup
    )
    return MAIN_MENU


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with all available commands"""
    help_text = """
Available commands:
/start - Start the bot and show main menu
/help - Show this help message
/cancel - Cancel current operation and return to main menu

Navigation:
- Use the buttons to navigate through menus
- Use 'Back' buttons to go to previous menus
- Use /cancel at any time to return to main menu

Features:
1. Manage Admins (Owner only):
   - Add new admins
   - View current admins
   - Remove admins

2. Manage URLs & Labels (Admins):
   - Add/Edit/Delete URLs
   - Add/Edit/Delete Labels
   - View all URLs and Labels

3. Create Posts (Admins):
   - Select or add new URL
   - Select or add new Label
   - Optional text and image
   - Preview before posting
"""
    await update.message.reply_text(help_text)


async def post_init(application: Application):
    """Set up bot commands"""
    commands = [
        BotCommand("start", "Start the bot and show main menu"),
        BotCommand("help", "Show help message with available commands"),
        BotCommand("cancel", "Cancel current operation and return to main menu"),
    ]
    await application.bot.set_my_commands(commands)


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(button_handler)],
            ADMIN_MENU: [CallbackQueryHandler(button_handler)],
            WAITING_FOR_ADMIN_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_id)
            ],
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
            WAITING_FOR_IMAGE: [
                MessageHandler(filters.PHOTO | filters.TEXT, handle_image)
            ],
            CONFIRM_POST: [CallbackQueryHandler(button_handler)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    # Set up commands
    application.post_init = post_init

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
