from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from firebase_admin import auth, initialize_app, credentials

from . import user_services, user_dtos, user_model
from app.utils import optional

load_dotenv()

"""
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CART_URL=https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4cs3r%40int-v1.iam.gserviceaccount.com
FIREBASE_UNIVERSE_DOMAIN=googleapis.com
"""

cred = credentials.Certificate({
    'type': os.environ.get('FIREBASE_TYPE'),
    'project_id': os.environ.get('FIREBASE_PROJECT_ID'),
    'private_key_id': os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    'private_key': os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    'client_email': os.environ.get('FIREBASE_CLIENT_EMAIL'),
    'client_id': os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
    "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER'),
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CART_URL'),
    "universe_domain": os.environ.get('FIREBASE_UNIVERSE_DOMAIN')
})
initialize_app(cred)


async def firebase_login(data: user_dtos.FirebaseLoginDto, db: Session) \
        -> optional.Optional[user_model.UserModel, HTTPException]:
    try:
        decoded_token = auth.verify_id_token(data.id_token)
        uid = decoded_token['uid']
        # decoded  email
        user_email = decoded_token.get('email')
        # return user get by email
        return user_services.get_user_by_email(db, email=user_email)

    except Exception as e:
        return optional.build(error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"))
