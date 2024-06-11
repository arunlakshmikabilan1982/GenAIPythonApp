import streamlit as st


st.title("Chat With AI")

# Load your images
image1 = "https://i0.wp.com/modernretail.co.uk/wp-content/uploads/2018/09/shutterstock_1067702951.png?fit=740%2C545&ssl=1"
image2 = "https://i0.wp.com/modernretail.co.uk/wp-content/uploads/2018/09/shutterstock_1067702951.png?fit=740%2C545&ssl=1"
image3 = "https://analyticsindiamag.com/wp-content/uploads/2020/05/chatbot_adoption.jpg"
image4 = "https://analyticsindiamag.com/wp-content/uploads/2020/05/chatbot_adoption.jpg"

# Display images in a square format using Streamlit's columns layout
col1, col2 = st.columns(2)

with col1:
    st.image(image1, caption='AI ChatBot', use_column_width=True)

    # Adjust size if necessary
    st.image(image3, caption='AI ChatBot', use_column_width=True)

with col2:
    st.image(image2, caption='AI ChatBot', use_column_width=True)

    # Adjust size if necessary
    st.image(image4, caption='AI ChatBot', use_column_width=True)


