import streamlit as st
from db import supabase

def show_login():
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;}</style>""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Market Screener</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sign in to continue</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Log In", use_container_width=True)
            
            if submit:
                if email and password: 
                    try:
                        # Raw Supabase query to authenticate the user
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        
                        if response.user:
                            st.session_state.logged_in = True
                            st.session_state.user_email = response.user.email
                            st.session_state.current_page = 'screener'
                            st.rerun()
                    except Exception:
                        st.error("Invalid email or password. Please try again.")
                else:
                    st.error("Please provide valid credentials.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("New user? Create an account", use_container_width=True):
            st.session_state.current_page = 'register'
            st.rerun()