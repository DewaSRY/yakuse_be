# from sqlalchemy.orm import Session
# from .business_model import Business
# from app.libs.sql_alchemy_lib import get_db

# def get_business_length(session: Session= next(get_db())) -> int:
#     return session.query(Business).count()


# def init_business(session: Session = next(get_db())):

#     pertanian = Business(
#         name="Bijih Kopi",
#         omset=50000000.0,
#         description="Bijih Kopi adalah kedai kopi yang menyediakan berbagai jenis kopi berkualitas tinggi yang berasal dari berbagai daerah di Indonesia. Dengan suasana yang nyaman dan pelayanan yang ramah, Bijih Kopi menjadi tempat favorit bagi pecinta kopi untuk bersantai dan menikmati secangkir kopi.",
#         photo_url="https://example.com/images/bijih_kopi.jpg",
#         location="Jl. Merdeka No. 45, Jakarta",
#         contact="+62 812-3456-7890",
#         fk_business_category_id=5,
#         fk_owner_id="98b6e7b3-910f-426d-a930-c7a37d1874dc"
#     )
#     kuliner = Business(
#         name="Warung Sate Pak Joko",
#         omset=70000000.0,
#         description="Warung Sate Pak Joko adalah tempat legendaris yang terkenal dengan sajian sate kambing dan ayam yang gurih dan lezat. Menggunakan resep turun-temurun dengan bumbu khas yang kaya rasa, warung ini menjadi tujuan favorit para pencinta kuliner di Jakarta.",
#         photo_url="https://example.com/images/warung_sate_pak_joko.jpg",
#         location="Jl. Kebon Jeruk No. 21, Jakarta",
#         contact="+62 812-9876-5432",
#         fk_business_category_id=1,
#         fk_owner_id="98b6e7b3-910f-426d-a930-c7a37d1874db"
#     )
#     kreatif = Business(
#         name="Batik Nusantara",
#         omset=150000000.0,
#         description="Batik Nusantara adalah usaha kreatif yang memproduksi dan menjual batik asli Indonesia dengan desain tradisional dan modern. Kami berkomitmen untuk melestarikan warisan budaya dengan menghadirkan koleksi batik yang unik dan berkualitas tinggi.",
#         photo_url="https://example.com/images/batik_nusantara.jpg",
#         location="Jl. Batik Indah No. 7, Yogyakarta",
#         contact="+62 812-9876-5432",
#         fk_business_category_id=3,
#         fk_owner_id="98b6e7b3-910f-426d-a930-c7a37d1874da"
#     )
#     jasa = Business(
#         name="Laundry Express",
#         omset=35000000.0,
#         description="Laundry Express adalah layanan laundry cepat dan profesional yang menawarkan cuci, setrika, dan pengantaran dalam waktu singkat. Dengan peralatan modern dan deterjen berkualitas, kami menjamin pakaian Anda bersih, rapi, dan wangi.",
#         photo_url="https://example.com/images/laundry_express.jpg",
#         location="Jl. Sudirman No. 12, Bandung",
#         contact="+62 812-1234-5678",
#         fk_business_category_id=4,
#         fk_owner_id="98b6e7b3-910f-426d-a930-c7a37d1874da"
#     )
#     pendidikan = Business(
#         name="Bimbingan Belajar Cerdas",
#         omset=80000000.0,
#         description="Bimbingan Belajar Cerdas adalah lembaga pendidikan yang menawarkan kursus tambahan untuk siswa SD hingga SMA. Kami memiliki pengajar berpengalaman dan metode pembelajaran yang efektif untuk membantu siswa meraih prestasi akademis terbaik.",
#         photo_url="https://example.com/images/bimbel_cerdas.jpg",
#         location="Jl. Pendidikan No. 15, Surabaya",
#         contact="+62 812-3456-7890",
#         fk_business_category_id=7,
#         fk_owner_id="98b6e7b3-910f-426d-a930-c7a37d1874db"
#     )

#     session.add_all([pertanian, kuliner, kreatif, jasa, pendidikan])
#     session.commit()
