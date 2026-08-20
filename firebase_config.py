import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Agar pehle se app initialize nahi hai, toh secrets ka use karke karein
if not firebase_admin._apps:
    # Streamlit secrets se Firebase credentials ko dictionary mein convert karein
    firebase_secrets = dict(st.secrets["FIREBASE"])
    
    # Certificate ko file ki jagah direct dictionary pass karein
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

# Firestore client initialize karein
db = firestore.client()
