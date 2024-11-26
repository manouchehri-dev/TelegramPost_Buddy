# Telegram_Post_Buddy

**Telegram_Post_Buddy** is a Python application with a user-friendly GUI for sending **text messages, images, and interactive inline buttons** to your Telegram channels. Built with `tkinter` and `Qt` for the interface and integrated with the Telegram Bot API, this tool simplifies creating and sending rich, engaging posts.

---

## Features

- **User-Friendly Interface**: Write and send messages quickly with an intuitive design.
- **Inline Buttons**: Add interactive buttons that link to websites or actions for enhanced engagement.
- **Image Upload Support**: Upload and preview images before sending them with or without captions.
- **Text and Captions**: Send text messages, image captions, or combine both.
- **Error Handling**: Alerts you about empty inputs or failed message deliveries.
- **Clear Image Option**: Reset the selected image and input fields effortlessly.

---

## Getting Started

### Prerequisites

1. Python 3.x installed on your system.
2. Required Python libraries:
   ```bash
   pip install python-telegram-bot pillow python-dotenv
   ```
   or
   ```bash
   pip install python-telegram-bot pillow python-dotenv PyQt5
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Telegram_Post_Buddy.git
   cd Telegram_Post_Buddy
   ```

3. Run the application:
   ```bash
   python telegram_post_buddy_tk.py
   ```
   or
   ```bash
   python telegram_post_buddy_qt.py
   ```

---

## How to Use

1. **Type Your Message**:
   - Enter your desired text in the provided text box.

2. **Upload an Image** (Optional):
   - Click the **"Upload Image"** button to select an image from your device.
   - The selected image will appear in the preview section.

3. **Add an Inline Button**:
   - Customize the button's text and URL to make your message interactive.
   - Example:
     - **Text**: "Learn More"
     - **URL**: `https://example.com`

4. **Send the Message**:
   - Click the **"Send Message"** button to post the message, image, and button to your Telegram channel.

---

## Demo

### Example Message

| **Feature**         | **Description**                     |
|----------------------|-------------------------------------|
| **Message Content**  | "Check out our new app!"           |
| **Image Preview**    | Displays the selected image in the GUI. |
| **Inline Button**    | Text: "Learn More", URL: `https://example.com` |

---

### Load Data Form .env
``` bash
BOT_TOKEN=YOUR_BOT_TOKEN
MINI_APP_URL=https://example.com
CHANNEL_NAME=@my_channel
BUTTON_LABEL=Play
```

## Contributing

Contributions are welcome! To contribute:

1. **Fork** the repository:
   ```bash
   git clone https://github.com/yourusername/Telegram_Post_Buddy.git
   ```
2. **Create a feature branch**:
   ```bash
   git checkout -b feature-name
   ```
3. **Make your changes** and commit them:
   ```bash
   git commit -m "Add description of your changes"
   ```
4. **Push your branch**:
   ```bash
   git push origin feature-name
   ```
5. **Open a Pull Request** with a detailed explanation of your changes.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## Support

If you encounter any issues or have feature requests, feel free to open an issue in the GitHub repository.
