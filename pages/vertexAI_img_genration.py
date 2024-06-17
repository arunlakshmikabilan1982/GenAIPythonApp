import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import streamlit as st
import numpy as np
from PIL import Image
import io
import tempfile
import os
import base64

# Define project information
PROJECT_ID = "serious-water-423304-j5"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
vertexai.init(project=PROJECT_ID, location=LOCATION)

st.markdown("<h1 style='text-align: center; color: violet;'>Image Generation</h1>", unsafe_allow_html=True)

generation_model = ImageGenerationModel.from_pretrained("imagegeneration@006")

prompt = st.text_input("Enter your thoughts to generate Image")
display_btn = st.button("Generate")
download_btn = st.button("Download Image")

def prompt_response():
    response = generation_model.generate_images(prompt=prompt)
    st.write(response)
    return response
if display_btn:

    response = prompt_response()    
    if len(response.images) > 0:
        generated_image = response.images[0]
        image_data_bytes = generated_image._loaded_bytes
        image_data = np.array(Image.open(io.BytesIO(image_data_bytes)))
        
        st.image(image_data, caption="Generated Image", use_column_width=True)
        
    else:
        st.write("Could not load the content")
if download_btn:
    response = prompt_response()   
    if len(response.images) > 0:
        generated_image = response.images[0] 
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            generated_image.save("Streamlit_genratedimage.png")
            st.write("Downloaded Successfully!")
    else:
        st.write("Could not load the content")
