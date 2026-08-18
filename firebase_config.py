import streamlit as st
from firebase_admin import credentials, initialize_app, firestore

# Check karo agar app pehle se initialized nahi hai toh initialize karo
if not st.session_state.get('firebase_initialized', False):
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    initialize_app(cred)
    st.session_state['firebase_initialized'] = True

db = firestore.client()
