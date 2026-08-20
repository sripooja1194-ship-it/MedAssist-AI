import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

if not firebase_admin._apps:
    try:
        # Secrets se raw JSON string nikalein aur use dictionary mein parse karein
        raw_json_str = st.secrets["FIREBASE"]["service_account"]
        service_account_info = json.loads(raw_json_str)
        
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Firebase Initialization Error: {e}")

db = firestore.client()
