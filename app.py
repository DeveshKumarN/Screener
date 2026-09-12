import streamlit as st
from login import show_login
from register import show_register
from screener import show_screener

def main():
    st.set_page_config(page_title="Pro Screener", layout="wide", initial_sidebar_state="collapsed")

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""

    # Route to the correct file's function
    if st.session_state.logged_in:
        show_screener()
    elif st.session_state.current_page == 'login':
        show_login()
    elif st.session_state.current_page == 'register':
        show_register()

if __name__ == "__main__":
    main()