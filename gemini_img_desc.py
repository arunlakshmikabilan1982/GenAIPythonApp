import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
import base64
from PIL import Image
import io

# Configure the Generative AI API
GEMINI_API_KEY = "YOUR_API_KEY"  # Replace "YOUR_API_KEY" with your actual API key
genai.configure(api_key=GEMINI_API_KEY)

# Streamlit app
st.title("Image to Text Converter")

# Input field for image upload
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

# Function to convert image to text
def convert_image_to_text(image):
    # Read the uploaded image
    img = Image.open(image)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Prompt template for image description
    prompt_template = """
    Describe the object in the image in detail, including market price, focusing on the objects, scene, colors, and composition.
    Provide detailed information on how to use and how it is manufactured.
    Answer the question: {question}. Do not answer any questions unrelated to the image.
    If you don't know the answer, mention "I don't have information regarding that."
    Thank you and feel free to come again!!
    """
    
    # Format the prompt with the input question
    prompt = PromptTemplate.from_template(template=prompt_template)
    input_question = "describe the object in the image"
    formatted_prompt = prompt.format(question=input_question)

    # Generate content using Generative AI API
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([formatted_prompt, img_byte_arr])

    # Return the generated text
    return response.text

# Convert image to text when "Convert" button is clicked
if st.button("Convert"):
    if uploaded_image is not None:
        text_output = convert_image_to_text(uploaded_image)
        st.success("Text generated from the image:")
        st.write(text_output)
    else:
        st.error("Please upload an image.")

