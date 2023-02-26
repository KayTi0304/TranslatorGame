from flask import Flask, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask_cors import CORS
from googletrans import Translator
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

chatbotEN = None
chatbotCH = None

class Chatbot:
    def __init__(self, model_name='microsoft/DialoGPT-medium'):
        self.model, self.tokenizer = self.load_model(model_name)
        self.chat_history = []
        self.chat_history_ids = None

    def load_model(self, model_name):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer

    def get_reply(self, user_message):
        now = datetime.now()
        self.chat_history.append({
            'text': user_message,
            'time': str(now.time().replace(microsecond=0))
        })
        message_ids = self.tokenizer.encode(user_message + self.tokenizer.eos_token, return_tensors='pt')
        if self.chat_history_ids is not None:
            message_ids = torch.cat([self.chat_history_ids, message_ids], dim=-1)

        self.chat_history_ids = self.model.generate(
            message_ids,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            max_length=1000,
            top_k=100,
            top_p=0.95,
            temperature=0.8
        )

        decoded_message = self.tokenizer.decode(
            self.chat_history_ids[:, message_ids.shape[-1]:][0],
            skip_special_tokens=True
        )

        self.chat_history.append({
            'text': decoded_message,
            'time': str(now.time().replace(microsecond=0))
        })

        return decoded_message
    
@app.route('/get-translation-prompt', methods=['GET', 'POST'])
def getTranslationPrompt():
    if request.method == 'POST':
        translator = Translator()
        data = request.get_json()
        textE = data.get('text')
        language = data.get('language')
        translated = translator.translate(text=textE, dest=language)
        print(translated)
        chat = {'text': translated.text}
        return jsonify(chat)


@app.route('/get-translation-language', methods=['GET', 'POST'])
def getTranslationLanguage():
    if request.method == 'POST':
        translator = Translator()
        data = request.get_json()
        textE = data.get('text')
        srcLn = data.get('srcLn')
        destLn = data.get('destLn')
        translated = translator.translate(text=textE, src=srcLn, dest=destLn)
        print(translated)
        chat = {'text': translated.text}
        return jsonify(chat)
    
@app.route('/get-translation', methods=['GET', 'POST'])
def getTranslation():
    if request.method == 'POST':
        data = request.get_json()
        textE = data.get('text')
        language = data.get('language')

        translator = Translator()
        
        chatbotCH = Chatbot()
        chatbotEN = Chatbot()

        if language == 'en':
            # 1. get a response from chatbot
            reply = chatbotEN.get_reply(textE)
            chat = {'text': reply}
            return jsonify(chat)

        else:
            # 1. translate desired language into en for chatbot
            translated = translator.translate(text=textE, dest='en')
            print(translated.text)
            # 2. get a response from chatbot
            reply = chatbotCH.get_reply(translated.text)
            # 3. Translate response to desired language
            reply2 = translator.translate(text=reply, dest=language)
            # 4. send data
            chat = {'text': reply2.text}
            return jsonify(chat)
            

@app.route('/')
def hello_world():
    return '<p>Hello world!</p>'

if __name__ == "__main__":
    app.run(debug=True)