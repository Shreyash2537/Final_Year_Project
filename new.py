from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
import sys
import os
import cv2
from PyQt5.QtGui import QPixmap
from googletrans import Translator 
from scene_description import SceneDescriptionThread  # Ensure this import is correct

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Navigator - DISHA")
        self.setGeometry(100, 100, 1650, 850)
        self.setStyleSheet("background-color: black;")
        
        # Background image
        self.bg = QLabel(self)
        pixmap = QPixmap("back.png")
        pixmap = pixmap.scaled(1650, 850, Qt.KeepAspectRatioByExpanding)
        self.bg.setPixmap(pixmap)
        self.bg.setGeometry(0, 0, 1650, 850)

        # Translator for multilingual support
        self.translator = Translator()

        # Supported languages
        self.languages = {'English': 'en', 'Hindi': 'hi', 'Spanish': 'es', 'French': 'fr'}
        self.selected_language = 'English'

        # Title label
        self.label_title = QLabel(self)
        self.label_title.setText("AI Navigator - DISHA")
        self.label_title.setStyleSheet("color: white; font-size: 48px; font-weight: bold; padding: 20px;")
        self.label_title.setAlignment(Qt.AlignCenter)
        self.label_title.move(0, 30)

        # Language dropdown menu
        self.language_menu = QComboBox(self)
        self.language_menu.addItems(self.languages.keys())
        self.language_menu.setCurrentText(self.selected_language)
        self.language_menu.setStyleSheet("font-size: 16px; background-color: gold; color: black; padding: 10px; border-radius: 5px;")
        self.language_menu.currentTextChanged.connect(self.change_language)
        self.language_menu.move(50, 50)

        # Feature buttons layout
        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        # Create buttons with hover effects
        self.create_hover_button("Text To Speech", self.button1)
        self.create_hover_button("Gesture To Voice", self.button2)
        self.create_hover_button("Voice To Text", self.button3)
        self.create_hover_button("Image To Voice", self.button4)
        self.create_hover_button("Object Detection", self.button5)
        self.create_hover_button("Scene Description", self.button6)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label_title)
        self.main_layout.addWidget(self.language_menu)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        # Scene Description Thread
        self.scene_thread = SceneDescriptionThread()
        self.scene_thread.update_frame_signal.connect(self.update_scene_description)
        self.scene_thread.update_caption_signal.connect(self.update_caption)

    def create_hover_button(self, text, command):
        button = QPushButton(text, self)
        button.setStyleSheet("background-color: lightgreen; color: black; font-size: 20px; font-weight: bold; padding: 10px; border-radius: 5px;")
        button.setFixedSize(200, 60)
        button.clicked.connect(command)
        button.setObjectName(text)

        # Add hover effect
        button.setStyleSheet("""
            QPushButton:hover {
                background-color: orange;
                color: red;
                width: 220px;
                height: 70px;
            }
        """)
        
        self.button_layout.addWidget(button)

    def change_language(self, lang):
        self.selected_language = lang
        self.translate_interface(lang)

    def translate_interface(self, language):
        target_lang = self.languages[language]
        self.label_title.setText(self.translator.translate("AI Navigator - DISHA", dest=target_lang).text)
        self.update_button_texts(target_lang)

    def update_button_texts(self, lang):
        button_texts = {
            "Text To Speech": "Text To Speech",
            "Gesture To Voice": "Gesture To Voice",
            "Voice To Text": "Voice To Text",
            "Image To Voice": "Image To Voice",
            "Object Detection": "Object Detection",
            "Scene Description": "Scene Description"
        }
        for button in self.findChildren(QPushButton):
            text = button.objectName()
            translated_text = self.translator.translate(button_texts[text], dest=lang).text
            button.setText(translated_text)

    def button1(self):
        os.system('python text_to_speech.py')

    def button2(self):
        os.system('python gesture_to_voice.py')

    def button3(self):
        os.system('python voice_to_text.py')

    def button4(self):
        os.system('python image_to_voice.py')

    def button5(self):
        os.system('python ObjectDetection.py')

    def button6(self):
        # Start the scene_description in a separate thread to avoid blocking the UI
        self.scene_thread.start()

    def update_scene_description(self, frame):
        """This method will handle the frame in the main thread to avoid OpenCV issues."""
        if frame is not None:
            try:
                cv2.imshow("Scene Description", frame)
                cv2.waitKey(1)  # Refresh the OpenCV window
            except Exception as e:
                print("OpenCV Error:", e)
        else:
            print("Invalid frame received")

    def update_caption(self, caption):
        """This method will handle the caption update in the UI or text-to-speech."""
        print("Updating caption:", caption)  # Debug print
        print(caption)  # You can display the caption in a QLabel or other UI element
        self.scene_thread.speak_caption(caption)  # Call the speak_caption method

    def closeEvent(self, event):
        self.scene_thread.stop()  # Stop the thread when closing the application
        cv2.destroyAllWindows()  # Ensure OpenCV window is properly closed
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())