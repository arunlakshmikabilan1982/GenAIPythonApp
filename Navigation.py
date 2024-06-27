import streamlit as st

def sidebar():
    option = st.sidebar.selectbox('Select Option', ['Requirement', 'Content AI','Development'])

    st.sidebar.header("Pages")

    if option == 'Requirement':
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Content_Generator" target="_self">Auto Pre-Sales Analysis</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Conversational_AI" target="_self">JIRA Stroy Analysis</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Conversational_AI" target="_self">Design Analysis</a>', unsafe_allow_html=True)

    elif option == 'Content AI':
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Train_your_Own_Data" target="_self">Train Your Own Data</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Content_Generator" target="_self">Content Generator</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Conversational_AI" target="_self">Conversational AI</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Image_To_Text_Description" target="_self">Image_To_Text_Description</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Language_Translator" target="_self">Language Translator</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/SEO_Generator-Assests" target="_self">SEO_Generator-Assests</a>', unsafe_allow_html=True)

    elif option == 'Development':
        
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Conversational_AI" target="_self">Conversational AI</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #1E88E5; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Image_To_Text_Description" target="_self">Devops AI</a>', unsafe_allow_html=True)
        

# Example usage
if __name__ == "__main__":
    sidebar()
