# Telegram_Post_Buddy

**Telegram_Post_Buddy** is a Python application with multiple interfaces for sending **text messages, images, and interactive inline buttons** to your Telegram channels. It offers three different implementations:
1. GUI with `tkinter`
2. GUI with `Qt`
3. Interactive Bot interface with `python-telegram-bot`

Built with modern Python frameworks and integrated with the Telegram Bot API, this tool simplifies creating and sending rich, engaging posts.

---

## Features

### GUI Applications (telegram_post_buddy_tk.py & telegram_post_buddy_qt.py)
- **User-Friendly Interface**: Write and send messages quickly with an intuitive design.
- **Inline Buttons**: Add interactive buttons that link to websites or actions for enhanced engagement.
- **Image Upload Support**: Upload and preview images before sending them with or without captions.
- **Text and Captions**: Send text messages, image captions, or combine both.
- **Error Handling**: Alerts you about empty inputs or failed message deliveries.
- **Clear Image Option**: Reset the selected image and input fields effortlessly.

### Bot Application (telegram_post_buddy_bot.py)
- **Interactive Bot Interface**: Control everything through Telegram commands and buttons
- **Admin Management**:
  - Owner can add/remove admins
  - View list of current admins
  - Admin permissions for posting
- **URL & Label Management**:
  - Store and reuse URLs and button labels
  - Edit/delete existing URLs and labels
  - Organize your content efficiently
- **Flexible Post Creation**:
  - Optional text and images
  - Reuse existing URLs and labels
  - Preview before posting
  - Back buttons at every stage
- **Command System**:
  - /start - Launch the main menu
  - /help - View all commands and features
  - /cancel - Return to main menu from any stage

---

## Getting Started

### Prerequisites

1. Python 3.x installed on your system.
2. Required Python libraries:
   ```bash
   # For GUI applications
   pip install python-telegram-bot pillow python-dotenv
   # For Qt GUI
   pip install python-telegram-bot pillow python-dotenv PyQt5
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Telegram_Post_Buddy.git
   cd Telegram_Post_Buddy
   ```

2. Run your preferred interface:
   ```bash
   # For Tkinter GUI
   python telegram_post_buddy_tk.py
   # For Qt GUI
   python telegram_post_buddy_qt.py
   # For Bot Interface
   python telegram_post_buddy_bot.py
   ```

---

## How to Use

### GUI Applications
1. **Type Your Message**:
   - Enter your desired text in the provided text box.
2. **Upload an Image** (Optional):
   - Click the **"Upload Image"** button to select an image from your device.
   - The selected image will appear in the preview section.
3. **Add an Inline Button**:
   - Customize the button's text and URL to make your message interactive.
4. **Send the Message**:
   - Click the **"Send Message"** button to post to your Telegram channel.

### Bot Application
1. **Start the Bot**:
   - Send /start to the bot
   - Access main menu with three options:
     - Manage Admins (owner only)
     - Manage URLs & Labels
     - Insert Post
2. **Managing Content**:
   - Add/edit/remove URLs and labels
   - Store frequently used links and button texts
3. **Creating Posts**:
   - Select or add new URL
   - Select or add new label
   - Optionally add text and image
   - Preview and confirm before sending
4. **Admin Management**:
   - Owner can add admins using their Telegram ID
   - View and remove admins as needed
   - Admins can create and send posts

---

## Configuration

### Load Data From .env
``` bash
BOT_TOKEN=YOUR_BOT_TOKEN
MINI_APP_URL=https://example.com
CHANNEL_NAME=@my_channel
BUTTON_LABEL=Play
OWNER_ID=your_telegram_user_id
CHANNEL_ID=@your_channel_name
```

---

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

Guidelines for contributions:
- Follow the existing code style and conventions
- Add comments to explain complex logic
- Update documentation for any new features
- Add appropriate error handling
- Test your changes thoroughly

---

## License

This project is licensed under the **MIT License**.

MIT License

Copyright (c) 2024 Telegram_Post_Buddy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Support

If you need help or have questions:

1. **GitHub Issues**:
   - Check existing issues for solutions
   - Open a new issue with detailed information about your problem
   - Include steps to reproduce any bugs
   - Provide system information and error messages

2. **Feature Requests**:
   - Use GitHub issues to suggest new features
   - Describe the feature and its benefits
   - Provide examples of use cases

3. **Documentation**:
   - Check the README for basic usage
   - Review code comments for detailed information
   - Ask for clarification if needed

4. **Contact**:
   - Use GitHub discussions for general questions
   - Tag relevant contributors in issues
   - Be clear and concise in communications

For security issues, please report them privately to the repository maintainers.

