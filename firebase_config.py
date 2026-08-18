import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

# Check karo agar Firebase pehle se initialize nahi hai
if not firebase_admin._apps:
    try:
        # Raw JSON string ko parse kar rahe hain
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        # Explicitly project_id pass kar rahe hain taaki environment variable ki zaroorat na pade
        initialize_app(cred, {'projectId': key_dict.get('project_id')})
    except Exception as e:
        # Agar secrets mein JSON nahi hai, toh direct values se try karega
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
        initialize_app(cred, {'projectId': cred_dict['project_id']})

db = firestore.client()
