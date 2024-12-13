import speech_recognition as sr
import tkinter as tk

class SpeechRecognitionGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Speech Recognition")
        
        self.text_box = tk.Text(self.root, height=10, width=50)
        self.text_box.pack()
        
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        
        self.recognition_count = 0
        self.recognition_list = []
        
        self.start_button = tk.Button(self.root, text="Start Recognition", command=self.start_recognition)
        self.start_button.pack()
        
        self.root.mainloop()
        
    def start_recognition(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.text_box.insert(tk.END, "Say something...\n")
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            self.text_box.insert(tk.END, f"You said: {text}\n")
            self.recognition_count += 1
            self.recognition_list.append(text)
            
            if self.recognition_count > 5:
                self.recognition_list.pop(0)
                self.recognition_count -= 1
                
            self.update_recognition_history()
            
        except sr.UnknownValueError:
            self.text_box.insert(tk.END, "Sorry, I could not understand what you said.\n")
        
    def update_recognition_history(self):
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, "Recognition History:\n")
        for i, recognition in enumerate(self.recognition_list):
            self.text_box.insert(tk.END, f"{i+1}. {recognition}\n")
SpeechRecognitionGUI()
