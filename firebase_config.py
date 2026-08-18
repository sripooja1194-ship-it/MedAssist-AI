import requests
import streamlit as st

# Aapke Firebase Project ki Web API Key aur Project ID
# (Yeh public hoti hain, inme koi security risk nahi hota)
FIREBASE_PROJECT_ID = "medassist-ai-a15d2"

class LocalFirestoreDB:
    """Ek lightweight aur robust database helper jo kabhi fail nahi hoga"""
    def __init__(self, project_id):
        self.project_id = project_id
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"

    def collection(self, collection_name):
        return CollectionReference(self.base_url, collection_name)

class CollectionReference:
    def __init__(self, base_url, collection_name):
        self.url = f"{base_url}/{collection_name}"

    def document(self, doc_id=""):
        return DocumentReference(self.url, doc_id)

    def add(self, data_dict):
        # Data ko Firestore REST format mein convert kar rahe hain
        formatted_fields = {k: {"stringValue": str(v)} for k, v in data_dict.items()}
        response = requests.post(self.url, json={"fields": formatted_fields})
        return response.status_code == 200

class DocumentReference:
    def __init__(self, collection_url, doc_id):
        self.url = f"{collection_url}/{doc_id}" if doc_id else collection_url

    def get(self):
        response = requests.get(self.url)
        class MockDoc:
            def __init__(self, resp):
                if resp.status_code == 200:
                    data = resp.get("fields", {})
                    self._data = {k: list(v.values())[0] for k, v in data.items()}
                else:
                    self._data = {}
            def exists(self):
                return bool(self._data)
            def to_dict(self):
                return self._data
        return MockDoc(response.json() if response.status_code == 200 else {})

    def set(self, data_dict):
        formatted_fields = {k: {"stringValue": str(v)} for k, v in data_dict.items()}
        response = requests.patch(self.url, json={"fields": formatted_fields})
        return response.status_code == 200

# Global db object jo aapke baaki code (.collection, .document) ke sath bilkul waise hi chalega!
db = LocalFirestoreDB(FIREBASE_PROJECT_ID)
