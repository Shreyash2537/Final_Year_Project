import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3
import tkinter as tk
from tkinter import simpledialog, messagebox

# Function to get text input from the user
def get_text_from_popup():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    user_input = simpledialog.askstring("Text-to-Speech", "Enter the text to convert to speech:")
    root.destroy()  # Destroy the tkinter window after getting input
    return user_input

# Function to get language selection from the user
def get_language_from_popup():
    root = tk.Tk()
    root.withdraw()
    languages = {
        "English": "en",
        "Hindi": "hi",
        "Spanish": "es",
        "French": "fr",
        "Kannada": "kan"
    }
    lang_options = "\n".join([f"{key}: {value}" for key, value in languages.items()])
    user_lang = simpledialog.askstring(
        "Language Selection",
        f"Choose a language (Enter code):\n{lang_options}"
    )
    root.destroy()
    return languages.get(user_lang.strip(), "en") if user_lang else "en"

# Main script
while True:
    try:
        # Get text input from the user
        text1 = get_text_from_popup()
        if not text1:  # If the user cancels or provides no input, exit the loop
            print("No input provided. Exiting...")
            break

        # Get language selection from the user
        lang = get_language_from_popup()

        print('\n------------Entered text--------------\n')
        print(f"Text: {text1}")
        print(f"Language: {lang}")

        # Convert text to speech and save as an MP3 file
        myobj = gTTS(text=text1, lang=lang, slow=False)
        myobj.save("voice.mp3")

        print('\n------------Playing--------------\n')
        song = MP3("voice.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load('voice.mp3')
        pygame.mixer.music.play()
        time.sleep(song.info.length)
        pygame.mixer.quit()

    except Exception as e:
        # Show error message if something goes wrong
        print(f"An error occurred: {e}")
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"An error occurred: {e}")
        root.destroy()
