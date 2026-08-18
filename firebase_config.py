import requests
import streamlit as st

# Firebase Web API Key aur Project ID jo aapke project ki hai
# Aap ise apne Firebase Console se le sakti hain ya direct use kar sakti hain
FIREBASE_PROJECT_ID = "medassist-ai-a15d2"

class SimpleFirestoreDB:
    """Firestore ke liye lightweight wrapper jo requests use karta hai"""
    def __init__(self, project_id):
        self.project_id = project_id
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"

    def get_document(self, collection, document_id):
        url = f"{self.base_url}/{collection}/{document_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    def add_document(self, collection, data_fields):
        url = f"{self.base_url}/{collection}"
        # Firestore REST format mein data convert kar rahe hain
        formatted_fields = {k: {"stringValue": str(v)} for k, v in data_fields.items()}
        payload = {"fields": formatted_fields}
        response = requests.post(url, json=payload)
        return response.status_code == 200

# Global db object jo poore app mein use hoga
db = SimpleFirestoreDB(FIREBASE_PROJECT_ID)
      
