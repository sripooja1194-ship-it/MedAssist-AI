import requests
import streamlit as st
from firebase_config import db

API_KEY = "AIzaSyAKVxCiQWnle9oHQavfghQDvzTl7vNMvr0"


def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    result = response.json()

    if "localId" in result:
        try:
            db.collection("users").document(result["localId"]).set({
                "email": email,
                "plan": "Free"
            })

            st.success("✅ Account created and Firestore saved!")

        except Exception as e:
            st.error(f"❌ Firestore Error: {e}")

    return result


def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    return response.json()
