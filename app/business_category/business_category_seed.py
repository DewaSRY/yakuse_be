from sqlalchemy.orm import Session

from .business_category_model import BusinessCategory

from app.libs.sql_alchemy_lib import get_db


def get_business_category_length(session: Session = next(get_db())) -> int:
    return session.query(BusinessCategory).count()


def init_business_category(session: Session = next(get_db())):
    kuliner = BusinessCategory(name="kuliner",
                               description="Bisnis kuliner adalah bisnis yang dijalankan di sektor kuliner atau makanan. Ini artinya menjual makanan ringan, makanan berat, sarapan, jajanan, termasuk minuman, dan semacamnya.")
    industri = BusinessCategory(name="industri",
                                description="Business industry adalah sektor ekonomi yang terdiri dari perusahaan yang memproduksi, menjual, atau menyediakan barang dan jasa.")
    kreative = BusinessCategory(name="kreative",
                                description="Bisnis kreatif adalah usaha yang menghasilkan keuntungan dari ide, inovasi, dan karya seni atau budaya.")
    jasa = BusinessCategory(name="jasa",
                            description="Bisnis jasa adalah usaha yang menawarkan layanan non-fisik, seperti konsultasi, perbankan, asuransi, dan pariwisata, untuk memperoleh keuntungan.")
    pertanian = BusinessCategory(name="pertanian",
                                 description="Bisnis pertanian adalah usaha yang berfokus pada produksi, pengolahan, dan penjualan produk hasil pertanian untuk keuntungan.")
    teknologi = BusinessCategory(name="teknologi",
                                 description="Bisnis teknologi adalah usaha yang mengembangkan, memproduksi, dan menjual produk atau layanan berbasis teknologi untuk keuntungan.")
    pendidikan = BusinessCategory(name="pendidikan",
                                  description="Bisnis pendidikan adalah sektor yang menyediakan layanan dan produk terkait pembelajaran, pelatihan, dan pengembangan keterampilan.")
    kesehatan = BusinessCategory(name="kesehatan",
                                 description="Bisnis kesehatan adalah usaha yang menyediakan layanan, produk, dan perawatan untuk meningkatkan dan memelihara kesehatan manusia.")
    transportasi = BusinessCategory(name="transportasi",
                                    description="Bisnis transportasi adalah usaha yang menyediakan layanan pengiriman barang dan orang dari satu tempat ke tempat lain.")
    properti = BusinessCategory(name="properti",
                                description="Bisnis properti adalah usaha yang membeli, menjual, menyewa, atau mengelola tanah dan bangunan untuk keuntungan.")
    session.add(kuliner)
    session.add(industri)
    session.add(kreative)
    session.add(jasa)
    session.add(pertanian)
    session.add(teknologi)
    session.add(pendidikan)
    session.add(kesehatan)
    session.add(transportasi)
    session.add(properti)
    session.commit()
