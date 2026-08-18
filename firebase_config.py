import streamlit as st
from firebase_admin import credentials, initialize_app, firestore

if not st.session_state.get('firebase_initialized', False):
    # Hum directly secrets ki values ko dictionary mein bhaar rahe hain
    cred_dict = {
        "type": st.secrets["firebase"]["type"],
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": st.secrets["firebase"]["auth_uri"],
        "token_uri": st.secrets["firebase"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
        "universe_domain": st.secrets["firebase"]["universe_domain"]
    }
    
    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)
    st.session_state['firebase_initialized'] = True

db = firestore.client()
