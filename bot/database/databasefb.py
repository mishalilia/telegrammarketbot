import firebase_admin
from firebase_admin import firestore


class Db:
    def __init__(self):
        self.app = firebase_admin.initialize_app()
        self.db = firestore.client()
