import streamlit as st
from supabase import create_client, Client

# Replace these with your actual Supabase Project URL and API Key
SUPABASE_URL = "https://iiaetbzeynfodpiygmom.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpYWV0YnpleW5mb2RwaXlnbW9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ5NzYwNDEsImV4cCI6MjEwMDU1MjA0MX0.22560KF9ckwWY4sdqIK-NxhMg0pSbSO_Bw_eBsSncXU"

@st.cache_resource
def init_connection() -> Client:
    """Initialize the Supabase client once and cache it for performance."""
    return create_client("https://iiaetbzeynfodpiygmom.supabase.co","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpYWV0YnpleW5mb2RwaXlnbW9tIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODQ5NzYwNDEsImV4cCI6MjEwMDU1MjA0MX0.22560KF9ckwWY4sdqIK-NxhMg0pSbSO_Bw_eBsSncXU")
supabase = init_connection()