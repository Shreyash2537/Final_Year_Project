import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import pyttsx3
import cv2
from PyQt5.QtCore import pyqtSignal, QThread
import numpy as np
import threading
from collections import deque
import time

# Load the pre-trained model
model = VisionEncoderDecoderModel.from_pretrained("models/vit-gpt2")
processor = ViTImageProcessor.from_pretrained("models/vit-gpt2")
tokenizer = AutoTokenizer.from_pretrained("models/vit-gpt2")

# Initialize Text-to-Speech
tts_engine = pyttsx3.init()

class SceneDescriptionThread(QThread):
    update_frame_signal = pyqtSignal(np.ndarray)
    update_caption_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.tts_speaking = False

    def run(self):
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.update_frame_signal.emit(frame)
                caption = self.generate_caption(frame)
                print("Emitting caption:", caption)  # Debug print
                self.update_caption_signal.emit(caption)
            time.sleep(1)  # Adjust the sleep time as needed
        cap.release()

    def generate_caption(self, frame):
        # Generate caption for the given frame
        # Ensure this logic is executed only once per frame
        # Return the generated caption
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        attention_mask = torch.ones(pixel_values.shape[:2], dtype=torch.long)

        # Generate caption using the model with attention_mask
        outputs = model.generate(pixel_values, attention_mask=attention_mask, max_length=50, num_beams=4)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def speak_caption(self, caption):
        """Speak the caption in a separate thread to avoid blocking the main thread."""
        if not self.tts_speaking:
            self.tts_speaking = True
            try:
                tts_engine.say(caption)
                tts_engine.runAndWait()
            except RuntimeError:
                print("Error: TTS engine is already speaking.")
            finally:
                self.tts_speaking = False

    def stop(self):
        self.running = False