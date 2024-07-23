import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os
import pygame

class GeminiPro:
    def __init__(self, api_key):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model_name = "models/gemini-1.5-flash"
        self.welcome_message = """Hey, How can I help you?"""

    def send_user_input(self, user_input):
        try:
            model = genai.GenerativeModel(self.model_name)
            chat = model.start_chat(history=[])
            response = chat.send_message(user_input)
            return response
        except Exception as err:
            print(f"Error occurred: {err}")
            return None

    def speak(self, text):
        tts = gTTS(text=text, lang='en')
        filename = "response.mp3"
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(filename)

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

    def run(self):
        print(self.welcome_message)
        self.speak(self.welcome_message)
        while True:
            user_input = self.listen()
            if user_input:
                print(f"You said: {user_input}")
                if user_input.lower() in ["exit", "quit", "bye"]:
                    goodbye_message = "Goodbye!"
                    print(goodbye_message)
                    self.speak(goodbye_message)
                    break
                response = self.send_user_input(user_input)
                if response and hasattr(response, 'text'):
                    print(response.text)
                    self.speak(response.text)
                else:
                    error_message = "Something went wrong. Please try again."
                    print(error_message)
                    self.speak(error_message)

if __name__ == "__main__":
    api_key = "Your_Gemini_Api_Key"  # Replace with your Gemini API key
    chatbot = GeminiPro(api_key)
    chatbot.run()
