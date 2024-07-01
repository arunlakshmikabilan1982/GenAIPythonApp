import streamlit as st

def sidebar():
    st.sidebar.markdown('<h1 style="color: #ffff; font-size: 32px; text-decoration: none; display: block; padding: 8px 0; margin-bottom: 10px; ">CMS AI COPILOT</a>', unsafe_allow_html=True)
    option = st.sidebar.selectbox('', ['Requirement', 'Content AI','Development'])

    st.sidebar.header("Pages")

    if option == 'Requirement':
        # st.sidebar.markdown('<a style="color: #498CC7; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Content_Generator" target="_self">Auto Pre-Sales Analysis</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/11083/11083341.png" width="45px" height="45px" style="margin-right: 10px;">Auto Pre-Sales Analysis</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/5968/5968875.png" width="45px" height="45px" style="margin-right: 10px;">JIRA Story Analysis</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/7991/7991055.png" width="45px" height="45px" style="margin-right: 10px;">Design Analysis</a>',unsafe_allow_html=True)
        

    elif option == 'Content AI':
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/2103/2103533.png" width="45px" height="45px" style="margin-right: 10px;">Train Your Own Data</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/11100/11100117.png" width="45px" height="45px" style="margin-right: 10px;">Content Generator</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/16210/16210772.png" width="45px" height="45px" style="margin-right: 10px;"> Conversational AI</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Image_To_Text_Description" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/5191/5191465.png" width="45px" height="45px" style="margin-right: 10px;"> Image To Text Description</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Language_Translator" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3898/3898150.png" width="45px" height="45px" style="margin-right: 10px;"> Language Translator</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/SEO_Generator-Assests" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/4335/4335889.png" width="45px" height="45px" style="margin-right: 10px;"> SEO Generator Assests</a>',unsafe_allow_html=True)

    elif option == 'Development':
        
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/SEO_Generator-Assests" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/1006/1006363.png" width="45px" height="45px" style="margin-right: 10px;">Code Generation AI</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/SEO_Generator-Assests" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/10906/10906860.png" width="45px" height="45px" style="margin-right: 10px;">Devops AI</a>',unsafe_allow_html=True)
        
        

# Example usage
if __name__ == "__main__":
    sidebar()

