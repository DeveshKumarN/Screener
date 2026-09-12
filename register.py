import streamlit as st
from db import supabase

def show_register():
    st.markdown("""<style>[data-testid="collapsedControl"] {display: none;}</style>""", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Create Account</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Join the platform today</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            email = st.text_input("Email Address")
            password = st.text_input("Password (min 6 characters)", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match!")
                elif email and password:
                    try:
                        # Raw Supabase database insert for new user
                        response = supabase.auth.sign_up({
                            "email": email, 
                            "password": password
                        })
                        if response.user:
                            st.success("Account created successfully! You can now log in.")
                        else:
                            st.info("Check your email for a confirmation link.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")
                else:
                    st.error("Please fill all fields.")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Already have an account? Log In", use_container_width=True):
            st.session_state.current_page = 'login'
            st.rerun()