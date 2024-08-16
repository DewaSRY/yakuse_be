from sqlalchemy.orm import Session

from .user_need_model import UserNeeds

from app.libs.sql_alchemy_lib import get_db


def get_user_need_length(session: Session = next(get_db())) -> int:
    return session.query(UserNeeds).count()


def init_user_need(session: Session = next(get_db())):
    a = UserNeeds(
        title="PO Nasi Goreng Spesial 40 Porsi",
        description="Dibutuhkan 40 porsi nasi goreng spesial dengan harga kisaran 15-25k/porsi untuk tanggal 17 Agustus 2024 di daerah Kebon Jeruk, Jakarta Tenggara",
        is_visible=True,
        fk_business_category_id=1,
        fk_user_id="1",
    )
    b = UserNeeds(
        title="Potong Rumput",
        description="Dibutuhkan jasa potong rumput untuk luas tanah 0,2 hektare secepatnya di daerah Bojongsoang, Jonggol",
        is_visible=True,
        fk_business_category_id=4,
        fk_user_id="1"
    )
    c = UserNeeds(
        title="Guru Les Privat Kimia untuk kelas 11",
        description="Dicari guru les privat matpel Kimia untuk kelas 11 di daerah Pondok Gede, Bogor",
        is_visible=True,
        fk_business_category_id=7,
        fk_user_id="2"
    )
    d = UserNeeds(
        title="Perawat untuk kanker end-stage",
        description="Dicari perawat laki-laki untuk merawat pasien laki-laki penderita kanker paru-paru di daerah Bintaro, Tangerang Tengah",
        is_visible=True,
        fk_business_category_id=8,
        fk_user_id="2"
    )
    # e = UserNeeds(
    #     title="",
    #     description="",
    #     is_visible=True,
    #     fk_business_category_id=1,
    #     fk_user_id=""
    # )

    
    session.add(a)
    session.add(b)
    session.add(c)
    session.add(d)
    # session.add(e)
    session.commit()
