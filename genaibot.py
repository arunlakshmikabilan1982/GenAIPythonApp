import google.generativeai as genai
from flask import Flask, json, request
app = Flask(__name__)

from environment import GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

@app.route('/askgenaibot', methods=['POST'])
def askgenaibot():
    data = json.loads(request.data)
    usertext = data['text']
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
    print("UserQuery:",usertext)
    response = model.generate_content(f"Generate Content {usertext}")
    return response.text

if __name__ == '__main__':
    #
    app.run(host="localhost", port=8000)
    