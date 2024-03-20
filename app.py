from flask import Flask, render_template, request, jsonify
from playsound import playsound
from googletrans import Translator
from gtts import gTTS
import os
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    # return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    r = sr.Recognizer() 
    with sr.Microphone() as source: 
        print("Speak Anything") 
        r.pause_threshold = 1
        audio = r.listen(source) 
        google_t = r.recognize_google(audio, language='en-in') 

    translator = Translator() 
    data = request.get_json()
    selected_value = data['selectedValue']
    print(selected_value) 
    
    to_lang = selected_value
    text_to_translate = translator.translate(google_t, dest=to_lang) 
    translated_text = text_to_translate.text 

    speak = gTTS(text=translated_text, lang=to_lang, slow=False) 
    speak.save("captured_voice.mp3") 
    playsound('captured_voice.mp3') 
    os.remove('captured_voice.mp3') 
    

    return render_template('translated.html', translated_text=translated_text)

if __name__ == '__main__':
    app.run(debug=True)
