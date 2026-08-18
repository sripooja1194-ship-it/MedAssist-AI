import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

# Firebase ko initialize karne ka standard aur safe tareeka
if not firebase_admin._apps:
    try:
        # Streamlit secrets se JSON load karna
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        initialize_app(cred)
    except Exception:
        # Agar JSON string nahi hai toh direct secrets dictionary use karein
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

# Asli Firestore client instance
db = firestore.client()
