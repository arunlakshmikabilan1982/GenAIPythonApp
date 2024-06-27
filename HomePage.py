import streamlit as st
from Navigation import sidebar

sidebar()

website_url = "https://automatic-succotash-7qw5p9pr9grcwrxj-8501.app.github.dev"

# Define the URLs of the images and the URLs of the pages you want to navigate to
image_urls = [
    ("https://www.cioinsight.com/wp-content/uploads/2022/08/Chatbots-in-Machine-Learning-scaled.jpeg", website_url+"/Conversational_Ai","Conversational AI"),
    ("https://tse2.mm.bing.net/th?id=OIP.MgRQ7QtM_TvVtnuwOnD-jAHaEK&pid=Api&P=0&h=220", website_url+"/Content_Generator","Content Generator"),
    ("https://analyticsindiamag.com/wp-content/uploads/2020/05/chatbot_adoption.jpg", website_url+"/Image_Description","Image To Text Description"),
    ("https://aviancetechnologies.com/wp-content/uploads/2022/05/free-meta-tag-generator.jpg", website_url+"/Seo_Generator","SEO Generator"),
    ("https://murf.ai/resources/media/posts/97/concept-program-smartphone-translate-from-different-languages.jpg", website_url+"/Language_Translator","Language Translator")
]


for image_url, page_url , name in image_urls[:5]:
    st.title(name+":")
    st.markdown(f"<a href='{page_url}' target='_blank'><img src='{image_url}' width='600' height='350'></a>", unsafe_allow_html=True)

