from sqlalchemy.orm import Session

from .user_model import UserModel

from app.libs.sql_alchemy_lib import get_db


def get_user_length(session: Session = next(get_db())) -> int:
    return session.query(UserModel).count()


def init_user(session: Session = next(get_db())):
    user_1 = UserModel(
        id="98b6e7b3-910f-426d-a930-c7a37d1874da",
        fullname="Dewa Maris",
        username="dewamaris",
        email="dewamaris@mail.co",
        hash_password="password",
        phone="+623454321",
        address="Jalan Sudirman No. 15, RT 01/01, Cinere Jaya, Banyuwangi, Bali",
        about_me="Saya memulai beberapa bidang bisnis setelah resign",
        photo_url=""
    )
    user_2 = UserModel(
        id="98b6e7b3-910f-426d-a930-c7a37d1874db",
        fullname="Iman Surya",
        username="imansurya",
        email="imansurya@mail.co",
        hash_password="password",
        phone="+6234543210",
        address="Jalan Juanda No. 15, RT 01/01, Cinere Jaya, Banyuwangi, Bali",
        about_me="Saya sedang merintis bimbel untuk SD-SMP-SMA dan bidang usaha rintisan sodara yaitu kuliner",
        photo_url=""
    )
    user_3 = UserModel(
        id="98b6e7b3-910f-426d-a930-c7a37d1874dc",
        fullname="Haikal Maris",
        username="haikalmaris",
        email="haikalmaris@mail.co",
        hash_password="password",
        phone="+62345432101",
        address="Jalan Gatot No. 15, RT 01/01, Cinere Jaya, Banyuwangi, Bali",
        about_me="Saya sedang memulai usaha dalam bidang pertanian dan kesehatan",
        photo_url=""
    )


    
    session.add(user_1)
    session.add(user_2)
    session.add(user_3)

    session.commit()
