import google.generativeai as genai
from flask import Flask, json, request
from environment import GEMINI_API_KEY
from langchain_core.prompts import PromptTemplate
import base64
from PIL import Image
import io

app = Flask(__name__)
genai.configure(api_key=GEMINI_API_KEY)

@app.route('/imgtotxt', methods=['POST'])  
def imagetotext():
      data = json.loads(request.data)
      byte = data.get('image')

      #By passing the decoded binary data to io.BytesIO, 
      #it essentially creates a temporary in-memory file containing the raw image data.
      
      image = Image.open(io.BytesIO(base64.decodebytes(bytes(byte, "utf-8"))))
      prompt_template: str = """
          Use below template to provide the Image details
          Template:
          Title-- eyecatching title for the image, should be atleast 5 words.
          Description-- All the important details like configuration, features about the image, Not to exceed 50 words.
          Keywords-- keywords for the image provided.
          role: SEO Metadata Content Creator
          question: {question}.
          """    
      prompt = PromptTemplate.from_template(template=prompt_template)
      input = "describe the object in the image with provided template and role"
      prompt_formatted_str: str = prompt.format(question=input)
      model = genai.GenerativeModel('gemini-pro-vision')
      response = model.generate_content([prompt_formatted_str,image])  
      return response.text
 
if __name__ == '__main__':
   app.run(host="localhost", port=8000, debug=True)   