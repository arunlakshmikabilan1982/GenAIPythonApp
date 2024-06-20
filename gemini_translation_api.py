import os
import google.generativeai as genai
from flask import Flask, json, request
from environment import GEMINI_API_KEY

app = Flask(__name__)

# Get the API key from the environment variables
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route('/aitranslator', methods=['POST']) 
def genaitranslator():
   data = json.loads(request.data)
   sourcelanguage = data['sourcelanguage']
   targetlanguage = data['targetlanguage']
   text = data['text']
   response = model.generate_content(f"Just Translate the sentence from language {sourcelanguage} to language {targetlanguage}: {text} and display only translated text")
   return response.text

if __name__ == '__main__':
    #
   app.run(host="localhost", port=8000)   
