import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import cv2
import openai
import tkinter as tk
from tkinter import scrolledtext

# Create a Tkinter window
window = tk.Tk()
window.title("HIYA - AI Desktop Assistant")
window.geometry("500x500")

# Create a label for the heading
heading_label = tk.Label(window, text="HIYA", font=("Arial", 20), fg="white", bg="black")
heading_label.pack(pady=10)

# Add colorful background and text style
window.configure(bg="white")
text_style = ("Helvetica", 14)

# Create a scrolled text widget for displaying conversation
conversation_text = scrolledtext.ScrolledText(window, width=60, height=28, bg="black", fg="white", font=text_style)
conversation_text.pack(pady=20)


# Function to speak the assistant's response
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)    
    if hour >= 0 and hour < 12:
        response = "Good Morning"
    elif hour >= 12 and hour < 16:
        response = "Good Afternoon"
    else:
        response = "Good evening"
    
    conversation_text.insert(tk.END, "Hiya: " + response + "\n")
    speak(response)

    response = "I am Hiya, How can I assist you, sir?"
    conversation_text.insert(tk.END, "Hiya: " + response + "\n")
    speak(response)

# Function to recognize user's speech
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        conversation_text.insert(tk.END, "Listening...\n")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            conversation_text.insert(tk.END, "Recognizing...\n")
            query = r.recognize_google(audio, language='en-in')
            conversation_text.insert(tk.END, "User: " + query + "\n")
            print("User:", query)
            return query
        except Exception as e:
            conversation_text.insert(tk.END, "Please Say Again\n")
            print("Please Say Again")
            return "None"

# Function to handle user queries
def handleQuery():
    query = takeCommand().lower()

    if 'wikipedia' in query:
        conversation_text.insert(tk.END, "Searching Wikipedia...\n")
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        conversation_text.insert(tk.END, "Hiya: According to Wikipedia\n" + results + "\n")
        speak("According to Wikipedia")
        speak(results)
    elif 'youtube' in query:
        conversation_text.insert(tk.END, "Hiya: Opening YouTube\n")
        speak('Opening YouTube')
        webbrowser.open("youtube.com")
    elif 'google' in query:
        conversation_text.insert(tk.END, "Hiya: Opening Google\n")
        speak('Opening Google')
        webbrowser.open("google.com")
    elif 'weather' in query:
        conversation_text.insert(tk.END, "Hiya: Getting Today's Weather\n")
        speak("Getting Today's Weather")
        webbrowser.open("https://www.google.com/search?q=weather&oq=weather&aqs=edge..69i57j0i273i650j0i131i433i512j0i131i433i650j0i131i433i457i512j0i402i650l2j0i131i433i512.8692j0j1&sourceid=chrome&ie=UTF-8")
    elif 'play music' in query:
        dir = 'E:\songs'
        song = os.listdir(dir)
        conversation_text.insert(tk.END, "Hiya: Playing Music...\n" + str(song) + "\n")
        speak('Playing Music')
        os.startfile(os.path.join(dir, song[0]))
    elif 'time' in query:
        Time = datetime.datetime.now().strftime("%H:%M:%S")
        conversation_text.insert(tk.END, "Hiya: Current Time is " + Time + "\n")
        speak(f"Current Time is {Time}")
    elif 'code' in query:
        path = "C:\\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        conversation_text.insert(tk.END, "Hiya: Opening Visual Studio Code...\n")
        speak("Opening Visual Studio Code...")
        os.startfile(path)
    elif 'file manager' in query:
        path = 'C:\\'
        conversation_text.insert(tk.END, "Hiya: Opening File Manager...\n")
        speak("Opening File Manager")
        os.startfile(path)
    elif 'camera' in query:
        conversation_text.insert(tk.END, "Hiya: Opening Camera...\n")
        speak("Opening Camera")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        response = queryChatGPT(query)
        conversation_text.insert(tk.END, "Hiya: " + response + "\n")
        speak(response)

# Bind the handleQuery function to a button click event
query_button = tk.Button(window, text="Give Command", command=handleQuery, bg="black", fg="white", font=text_style)
query_button.pack(pady=10)

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

# Function to interact with ChatGPT for queries
def queryChatGPT(query):
    prompt = "User: {}\nAssistant:".format(query)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
        api_key='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'
        # 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-2
        # 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-1
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    wishMe()
    window.mainloop()
