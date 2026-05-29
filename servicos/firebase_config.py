import firebase_admin

from firebase_admin import (
    credentials,
    firestore
)

# ==========================================
# INICIALIZA FIREBASE APENAS UMA VEZ
# ==========================================

if not firebase_admin._apps:

    cred = credentials.Certificate(
        "firebase-chave.json"
    )

    firebase_admin.initialize_app(cred)

# ==========================================
# FIRESTORE
# ==========================================

db = firestore.client()