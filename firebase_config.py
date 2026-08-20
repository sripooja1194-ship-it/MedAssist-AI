import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# अगर पहले से ऐप इनिशियलाइज नहीं है, तो करें
if not firebase_admin._apps:
    # (ध्यान दें: आपके पास serviceAccountKey.json फाइल होनी चाहिए, 
    # जिसे आप Firebase Console -> Project Settings -> Service Accounts से डाउनलोड करती हैं)
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# सीधा ऑफिशियल Firestore क्लाइंट
db = firestore.client()
