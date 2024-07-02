import streamlit as st

def init_session_state():
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = 'REQUIREMENT AI'


def sidebar():
#     hide_st_style="""
#                     <style>
#                     #MainMenu {visibilty:hidden;}
#                     footer {visibilty:hidden;}
#                     header {visibilty:hidden;}
#                     </style>
#                     """
#     st.markdown(hide_st_style,unsafe_allow_html=True)

    init_session_state()
    
    # Update session state based on URL parameters
    query_params = st.query_params
    if 'option' in query_params:
        st.session_state.selected_option = query_params['option']

    st.sidebar.markdown('<h1 style="color: #ffff; font-size: 32px; text-decoration: none; display: block; padding: 8px 0; margin-bottom: 10px; ">CMS AI COPILOT</a>', unsafe_allow_html=True)
    options = ['REQUIREMENT AI', 'CONTENT AI', 'DEVELOPMENT AI']
    selected_index = options.index(st.session_state.selected_option) if st.session_state.selected_option in options else 0
    option = st.sidebar.selectbox('Select Page', options, index=selected_index)
    st.sidebar.header("Pages")

    if option == 'REQUIREMENT AI':
        # st.sidebar.markdown('<a style="color: #498CC7; font-size: 16px; text-decoration: none; display: block; padding: 8px 0;" href="/Content_Generator" target="_self">Auto Pre-Sales Analysis</a>', unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="auto_presale_analysis?option=REQUIREMENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/11083/11083341.png" width="45px" height="45px" style="margin-right: 10px;">Auto Pre-Sales Analysis</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Jira_story_generator?option=REQUIREMENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/5968/5968875.png" width="45px" height="45px" style="margin-right: 10px;">JIRA Story Generator</a>',unsafe_allow_html=True)
        # st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/Conversational_AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/7991/7991055.png" width="45px" height="45px" style="margin-right: 10px;">Design Analysis</a>',unsafe_allow_html=True)
        

    elif option == 'CONTENT AI':
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Train_Your_Own_Data?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3270/3270865.png" width="45px" height="45px" style="margin-right: 10px;">Train Your Own Data</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Content_Generator?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/11100/11100117.png" width="45px" height="45px" style="margin-right: 10px;">Content Generator</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Conversational_AI?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/16210/16210772.png" width="45px" height="45px" style="margin-right: 10px;"> Conversational AI</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Image_To_Text_Description?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/5191/5191465.png" width="45px" height="45px" style="margin-right: 10px;"> Image To Text Description</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Language_Translator?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/3898/3898150.png" width="45px" height="45px" style="margin-right: 10px;"> Language Translator</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Language_Translator_in_file?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/5798/5798224.png" width="45px" height="45px" style="margin-right: 10px;"> Language Translator with File</a>',unsafe_allow_html=True)
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="SEO_Generator-Assests?option=CONTENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/4335/4335889.png" width="45px" height="45px" style="margin-right: 10px;"> SEO Generator Assests</a>',unsafe_allow_html=True)

    elif option == 'DEVELOPMENT AI':
        
        st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="Code_Generator?option=DEVELOPMENT AI" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/1006/1006363.png" width="45px" height="45px" style="margin-right: 10px;">Code Generation AI</a>',unsafe_allow_html=True)
        # st.sidebar.markdown('<a style="color: #FFFF ; font-size: 16px; text-decoration: none; display: flex; align-items: center; padding: 8px 0;" href="/SEO_Generator-Assests" target="_self"><img src="https://cdn-icons-png.flaticon.com/128/10906/10906860.png" width="45px" height="45px" style="margin-right: 10px;">Devops AI</a>',unsafe_allow_html=True)
        
    st.sidebar.markdown('<script>window.history.pushState({}, "", window.location.pathname + "?option=" + encodeURIComponent("' + option + '"));</script>', unsafe_allow_html=True)

# Example usage
if __name__ == "__main__":
    sidebar()

