import requests
import streamlit as st

FIREBASE_PROJECT_ID = "medassist-ai-a15d2"

class LocalFirestoreDB:
    def __init__(self, project_id):
        self.project_id = project_id
        self.base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"

    def collection(self, collection_name):
        return CollectionReference(self.base_url, collection_name)

class CollectionReference:
    def __init__(self, base_url, collection_name):
        self.url = f"{base_url}/{collection_name}"
        self.query_filters = []

    def document(self, doc_id=""):
        return DocumentReference(self.url, doc_id)

    def where(self, field, op, value):
        # Query filtering support ke liye
        self.query_filters.append((field, op, value))
        return self

    def stream(self):
        # User data fetch karne ke liye stream() method
        res = requests.get(self.url)
        docs = []
        if res.status_code == 200:
            documents = res.json().get("documents", [])
            for doc in documents:
                doc_path = doc.get("name", "")
                doc_id = doc_path.split("/")[-1]
                fields = doc.get("fields", {})
                data_dict = {k: list(v.values())[0] for k, v in fields.items()}
                
                # Agar .where() filter lagaya gaya hai toh match check karein
                match = True
                for field, op, val in self.query_filters:
                    if data_dict.get(field) != val:
                        match = False
                        break
                if match:
                    docs.append(MockDocumentSnapshot(doc_id, data_dict))
        return docs

    def add(self, data_dict):
        formatted_fields = {k: {"stringValue": str(v)} for k, v in data_dict.items()}
        res = requests.post(self.url, json={"fields": formatted_fields})
        return res.status_code == 200

class MockDocumentSnapshot:
    def __init__(self, doc_id, data_dict):
        self.id = doc_id
        self._data = data_dict

    def to_dict(self):
        return self._data

    def exists(self):
        return bool(self._data)

class DocumentReference:
    def __init__(self, collection_url, doc_id):
        self.url = f"{collection_url}/{doc_id}" if doc_id else collection_url

    def get(self):
        res = requests.get(self.url)
        class MockDoc:
            def __init__(self, resp):
                if resp.status_code == 200:
                    data = resp.json().get("fields", {})
                    self._data = {k: list(v.values())[0] for k, v in data.items()}
                else:
                    self._data = {}
            def exists(self):
                return bool(self._data)
            def to_dict(self):
                return self._data
        return MockDoc(res)

    def set(self, data_dict, merge=False):
        formatted_fields = {k: {"stringValue": str(v)} for k, v in data_dict.items()}
        res = requests.patch(self.url, json={"fields": formatted_fields})
        return res.status_code == 200

db = LocalFirestoreDB(FIREBASE_PROJECT_ID)
