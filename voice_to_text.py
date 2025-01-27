import speech_recognition as sr
import tkinter as tk
from tkinter import simpledialog, messagebox

class SpeechRecognitionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speech Recognition")
        
        # Text box to display recognition results
        self.text_box = tk.Text(self.root, height=15, width=60, wrap=tk.WORD)
        self.text_box.pack(pady=10)
        
        # Buttons for actions
        self.start_button = tk.Button(self.root, text="Start Recognition", command=self.start_recognition)
        self.start_button.pack(pady=5)
        
        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_text_box)
        self.clear_button.pack(pady=5)
        
        # Speech recognizer and settings
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        
        # Recognition history
        self.recognition_history_limit = 5  # Configurable limit for history
        self.recognition_list = []
        
        # Language setting
        self.language = "en-US"  # Default language is English
        self.set_language_button = tk.Button(self.root, text="Set Language", command=self.set_language)
        self.set_language_button.pack(pady=5)
        
        self.root.mainloop()

    def start_recognition(self):
        try:
            # Listen to the user's voice
            with sr.Microphone() as source:
                self.text_box.insert(tk.END, "Adjusting for ambient noise...\n")
                self.recognizer.adjust_for_ambient_noise(source)
                self.text_box.insert(tk.END, "Say something...\n")
                audio = self.recognizer.listen(source)
            
            # Recognize speech using Google API
            text = self.recognizer.recognize_google(audio, language=self.language)
            self.text_box.insert(tk.END, f"You said: {text}\n")
            
            # Update recognition history
            self.recognition_list.append(text)
            if len(self.recognition_list) > self.recognition_history_limit:
                self.recognition_list.pop(0)
            self.update_recognition_history()
        
        except sr.UnknownValueError:
            self.text_box.insert(tk.END, "Sorry, I could not understand what you said.\n")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not connect to recognition service: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def update_recognition_history(self):
        # Display recognition history
        self.text_box.insert(tk.END, "\nRecognition History:\n")
        for i, recognition in enumerate(self.recognition_list):
            self.text_box.insert(tk.END, f"{i + 1}. {recognition}\n")

    def clear_text_box(self):
        # Clear the text box
        self.text_box.delete("1.0", tk.END)

    def set_language(self):
        # Allow user to set the recognition language
        languages = {
            "English (US)": "en-US",
            "Hindi": "hi-IN",
            "Kannada": "kn-IN",
            "Spanish": "es-ES",
            "French": "fr-FR"
        }
        lang_options = "\n".join([f"{key}: {value}" for key, value in languages.items()])
        lang_code = simpledialog.askstring("Set Language", f"Choose a language (Enter code):\n{lang_options}")
        
        if lang_code in languages.values():
            self.language = lang_code
            messagebox.showinfo("Language Set", f"Recognition language set to: {lang_code}")
        else:
            messagebox.showwarning("Invalid Language", "Invalid language code. Defaulting to English (US).")
            self.language = "en-US"

# Run the application
SpeechRecognitionGUI()
