import json
import streamlit as st
from firebase_admin import credentials, initialize_app, firestore

if not st.session_state.get('firebase_initialized', False):
    # Secrets se direct raw JSON string uthakar parse kar rahe hain
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])

    cred = credentials.Certificate(key_dict)
    initialize_app(cred)
    st.session_state['firebase_initialized'] = True

db = firestore.client()
