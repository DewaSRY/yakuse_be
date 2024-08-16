from sqlalchemy.orm import Session

from .user_model import UserModel

from app.libs.sql_alchemy_lib import get_db


def get_user_length(session: Session = next(get_db())) -> int:
    return session.query(UserModel).count()


def init_user(session: Session = next(get_db())):
    user_1 = UserModel(
        id="1",
        fullname="Dewa Maris",
        username="dewamaris",
        hash_password="password",
        phone="+623454321",
        address="Jalan Sudirman No. 15, RT 01/01, Cinere Jaya, Banyuwangi, Bali",
        about_me="Saya sedang merintis usaha es doger",
        photo_url=""
    )
    user_2 = UserModel(
        id="2",
        fullname="Iman Surya",
        username="imansurya",
        hash_password="password",
        phone="+6234543210",
        address="Jalan Juanda No. 15, RT 01/01, Cinere Jaya, Banyuwangi, Bali",
        about_me="Saya sedang merintis bimbel untuk SD-SMP-SMA",
        photo_url=""
    )

    
    session.add(user_1)
    session.add(user_2)

    session.commit()
