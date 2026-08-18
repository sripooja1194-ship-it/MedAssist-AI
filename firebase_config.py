import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

# Check karo agar Firebase pehle se initialize nahi hai
if not firebase_admin._apps:
    # Streamlit secrets se sirf FIREBASE_JSON load karenge
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(key_dict)
    initialize_app(cred)

# Asli Firestore client jo aapke baaki code (.collection wali queries) ke sath 100% chalega
db = firestore.client()
