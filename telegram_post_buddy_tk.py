import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import os
from dotenv import load_dotenv

# Initialize global variable for the image file path
image_path = None


# Load environment variables from .env file if selected
def load_env_variables():
    load_dotenv()
    token_input.delete(0, tk.END)
    channel_input.delete(0, tk.END)
    mini_app_input.delete(0, tk.END)
    button_label_input.delete(0, tk.END)
    token_input.insert(0, os.getenv("BOT_TOKEN", ""))
    channel_input.insert(0, os.getenv("CHANNEL_NAME", ""))
    mini_app_input.insert(0, os.getenv("MINI_APP_URL", ""))
    button_label_input.insert(0, os.getenv("BUTTON_LABEL", "Open Mini App"))
    messagebox.showinfo("Info", "Loaded credentials from .env file.")


# Function to send the message, image, and inline button
async def async_send_message(token, channel, message, mini_app_url, button_label):
    try:
        bot = Bot(token=token)

        # Create inline button for the mini app
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(button_label, url=mini_app_url)]]
        )

        if image_path:
            with open(image_path, "rb") as photo:
                await bot.send_photo(
                    chat_id=channel,
                    photo=photo,
                    caption=message,
                    reply_markup=reply_markup,
                )
        else:
            await bot.send_message(
                chat_id=channel, text=message, reply_markup=reply_markup
            )

        messagebox.showinfo("Success", "Message sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send message: {e}")


def send_message():
    global image_path
    token = token_input.get().strip()
    channel = channel_input.get().strip()
    message = text_input.get("1.0", tk.END).strip()
    mini_app_url = mini_app_input.get().strip()
    button_label = button_label_input.get().strip()

    if not token or not channel or not message or not mini_app_url or not button_label:
        messagebox.showerror(
            "Error",
            "Bot Token, Channel Name, Message, Mini App URL, and Button Label are required!",
        )
        return

    # Run the async send message function
    asyncio.run(async_send_message(token, channel, message, mini_app_url, button_label))


# Function to upload an image
def upload_image():
    global image_path
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )
    if image_path:
        # Load and display the selected image
        img = Image.open(image_path)
        img.thumbnail((150, 150))  # Resize the image for display
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        image_label.pack(pady=10)


# Function to clear all inputs
def clear_inputs():
    global image_path
    token_input.delete(0, tk.END)
    channel_input.delete(0, tk.END)
    text_input.delete("1.0", tk.END)
    mini_app_input.delete(0, tk.END)
    button_label_input.delete(0, tk.END)
    image_label.config(image="")
    image_label.image = None
    image_path = None


# Set up the Tkinter GUI
root = tk.Tk()
root.title("Telegram Mini App Sender")
root.geometry("400x800")

# Button to load credentials from .env
env_button = tk.Button(
    root, text="Load from .env File", font=("Arial", 12), command=load_env_variables
)
env_button.pack(pady=5)

# Input for Telegram Bot Token
tk.Label(root, text="Telegram Bot Token:", font=("Arial", 12)).pack(pady=5)
token_input = tk.Entry(root, width=40, font=("Arial", 12))
token_input.pack(pady=5)

# Input for Telegram Channel Name
tk.Label(root, text="Telegram Channel Name (@channel):", font=("Arial", 12)).pack(
    pady=5
)
channel_input = tk.Entry(root, width=40, font=("Arial", 12))
channel_input.pack(pady=5)

# Input for Telegram Mini App URL
tk.Label(root, text="Telegram Mini App URL:", font=("Arial", 12)).pack(pady=5)
mini_app_input = tk.Entry(root, width=40, font=("Arial", 12))
mini_app_input.pack(pady=5)

# Input for Button Label
tk.Label(root, text="Mini App Button Label:", font=("Arial", 12)).pack(pady=5)
button_label_input = tk.Entry(root, width=40, font=("Arial", 12))
button_label_input.pack(pady=5)

# Label and Textbox for Message
tk.Label(root, text="Write Your Message:", font=("Arial", 12)).pack(pady=5)
text_input = tk.Text(root, wrap="word", height=10, width=40)
text_input.pack(pady=5)

# Button to upload an image
upload_button = tk.Button(
    root, text="Upload Image", font=("Arial", 12), command=upload_image
)
upload_button.pack(pady=5)

# Label for displaying the selected image
image_label = tk.Label(root)
image_label.pack()

# Send button
send_button = tk.Button(
    root, text="Send Message", font=("Arial", 12), command=send_message
)
send_button.pack(pady=10)

# Clear inputs button
clear_button = tk.Button(
    root, text="Clear Inputs", font=("Arial", 12), command=clear_inputs
)
clear_button.pack(pady=5)

# Run the GUI application
root.mainloop()
