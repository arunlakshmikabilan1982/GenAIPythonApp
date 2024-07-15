from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from langchain import PromptTemplate
from Navigation import sidebar


sidebar()

# Load environment variables (if necessary)
# load_dotenv()

# Load API key securely from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Set Streamlit page configuration
# st.set_page_config(page_title="Description of Products", page_icon="📸")

# Define prompt template for image description
prompt_template: str = """/
Use the following pieces of context to answer the question {question}, assume AI role as "Image Analyzer and Requirements generator, Image analyser for component development requirements"

Identify the component from provided image and Provide Detailed component development Requirements and Code, use below format:
Requirements: Identify the component from the image, Component level description about image, ex: if image contains "image, text" analyse the image to get the requirements to develop it has a Component any tech.
Acceptance Criteria : Mention all the possible "acceptance criteria" that can gathered from the image. ex: If Image contains, Image, text on top and looks like carousel, mention about carousel component generic acceptance criteria
"""
prompt = PromptTemplate.from_template(template=prompt_template)

model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Function to get Gemini AI response based on image and prompt
def get_gemini_response(prompt_formatted_str, image):
    if prompt_formatted_str != "":
        response = model.generate_content([prompt_formatted_str, image])
    else:
        response = model.generate_content(image)
    return response.text

# Streamlit UI
st.header("Design to UI Code Generation")

# Placeholder input for initial prompt
input_prompt = "Describe the object in the image in detail to provide the details regarding component development"
prompt_formatted_str: str = prompt.format(question=input_prompt)

# File upload section for image
uploaded_file = st.file_uploader("Please select the Image", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

platform_templates = {
    "React": {
        "prompt_template": """Generate a React component for the given requirements: {input_query}, Provide Meaningfull Component Name.
### Explanation of Each Section:

1. **REQUIREMENTS:**
   - **Language/Platform:** Specify the programming language or platform for the code.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any dependencies or libraries required for the code.

2. **SOLUTION:** 
   - Consider AI role as "Code Generator in React" and Generate Code for {input_query} with React and if required include Code for supported technologies like CSS and JS and Explain about the required Code, Use markdown code blocks to format the code appropriately.

3. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.
"""
    },

    "Html and CSS": {
        "prompt_template": """Generate a Html and CSS, Javascript component for the given requirements: {input_query}.
### Explanation of Each Section:

1. **REQUIREMENTS:**
   - **Language/Platform:** Specify the programming language or platform for the code.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any dependencies or libraries required for the code.

2. **SOLUTION:** 
   - Consider AI role as "Code Generator in Html and CSS, Javascript" and Generate Code for {input_query} with Html and CSS, Javascript and Explain about the required Code, Use markdown code blocks to format the code appropriately.

3. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.
"""
    },

        "Angular": {
        "prompt_template": """Generate a Angular component for the given requirements: {input_query}.
### Explanation of Each Section:

1. **REQUIREMENTS:**
   - **Language/Platform:** Specify the programming language or platform for the code.
   - **Functionality/Feature:** Describe the specific functionality or feature needed.
   - **Dependencies:** List any dependencies or libraries required for the code.

2. **SOLUTION:** 
   - Consider AI role as "Code Generator in Angular" and Generate Code for {input_query} with Angular and if required include Code for supported technologies like CSS and JS and Explain about the required Code, Use markdown code blocks to format the code appropriately.

3. **RESOURCES:**
   - Include references to any sources or relevant resources.
     - Format each reference as `[Source](link)`.
"""
    }
    
}


category = st.radio("Please Select The Frontend Stack ", ["React", "Html and CSS", "Angular"])

if category == "React":
   selected_platform = "React"
if category == "Html and CSS":
   selected_platform = "Html and CSS"
if category == "Angular":
   selected_platform = "Angular"    

# Button to trigger Code Generation
if st.button("Generate Component Details and Code"):
    if image is not None:
        # Display loading spinner while generating response
        with st.spinner("Generating Requirements and Code..."):
            response = get_gemini_response(prompt_formatted_str, image)
        # Display response
        input_query =  response
        if input_query and selected_platform:
         platform_text = platform_templates[selected_platform]["prompt_template"].format(input_query=input_query)
         with st.spinner("Generating Requirements and Code..."):
          responsecode = model.generate_content(platform_text)
         if responsecode.candidates[0].content.parts[0] is not None:
            st.markdown(responsecode.candidates[0].content.parts[0].text, unsafe_allow_html=True)
        else:
         st.error("The details provided are invalid.")
    else:
        st.warning("Please ensure to upload an image first.")
