import sys
import asyncio
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QDesktopWidget,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os


# Initialize global variable for the image file path
image_path = None


class TelegramSenderApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the UI
        self.setWindowTitle("Telegram Mini App Sender")
        self.resize(1000, 1300)  # Set window size
        self.center()  # Center the window

        # Create layout
        self.layout = QVBoxLayout()

        # Load from .env button
        self.env_button = QPushButton("Load from .env File")
        self.env_button.clicked.connect(self.load_env_variables)
        self.layout.addWidget(self.env_button)

        # Input fields
        self.token_label = QLabel("Telegram Bot Token:")
        self.layout.addWidget(self.token_label)
        self.token_input = QLineEdit()
        self.layout.addWidget(self.token_input)

        self.channel_label = QLabel("Telegram Channel Name (@channel):")
        self.layout.addWidget(self.channel_label)
        self.channel_input = QLineEdit()
        self.layout.addWidget(self.channel_input)

        self.mini_app_label = QLabel("Telegram Mini App URL:")
        self.layout.addWidget(self.mini_app_label)
        self.mini_app_input = QLineEdit()
        self.layout.addWidget(self.mini_app_input)

        # Message input
        self.message_label = QLabel("Write Your Message:")
        self.layout.addWidget(self.message_label)
        self.message_input = QTextEdit()
        self.layout.addWidget(self.message_input)

        # Upload image button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

        # Image preview (centered)
        self.image_preview_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_preview_layout.addWidget(self.image_label)
        self.layout.addLayout(self.image_preview_layout)

        # Send message button
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Clear inputs button
        self.clear_button = QPushButton("Clear Inputs")
        self.clear_button.clicked.connect(self.clear_inputs)
        self.layout.addWidget(self.clear_button)

        # Set layout
        self.setLayout(self.layout)

    def center(self):
        """Center the window on the screen."""
        screen_geometry = QDesktopWidget().availableGeometry().center()
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(screen_geometry)
        self.move(frame_geometry.topLeft())

    def load_env_variables(self):
        load_dotenv()
        self.token_input.setText(os.getenv("BOT_TOKEN", ""))
        self.channel_input.setText(os.getenv("CHANNEL_NAME", ""))
        self.mini_app_input.setText(os.getenv("MINI_APP_URL", ""))
        QMessageBox.information(self, "Info", "Loaded credentials from .env file.")

    def upload_image(self):
        global image_path
        image_path, _ = QFileDialog.getOpenFileName(
            self, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)"
        )
        if image_path:
            pixmap = QPixmap(image_path).scaled(300, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    async def async_send_message(self, token, channel, message, mini_app_url):
        try:
            bot = Bot(token=token)
            # Inline keyboard for mini app
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton("Open Mini App", url=mini_app_url)]]
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

            QMessageBox.information(self, "Success", "Message sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send message: {e}")

    def send_message(self):
        token = self.token_input.text().strip()
        channel = self.channel_input.text().strip()
        message = self.message_input.toPlainText().strip()
        mini_app_url = self.mini_app_input.text().strip()

        if not token or not channel or not message or not mini_app_url:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        asyncio.run(self.async_send_message(token, channel, message, mini_app_url))

    def clear_inputs(self):
        global image_path
        self.token_input.clear()
        self.channel_input.clear()
        self.mini_app_input.clear()
        self.message_input.clear()
        self.image_label.clear()
        image_path = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelegramSenderApp()
    window.show()
    sys.exit(app.exec_())
