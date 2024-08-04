# Yasuke Be

## What is the app about ?

...

## Gimana cara running appnya ?

> jika kamu ingin mendevelop app in, pastikan docker compose usdah berjalan. docker compose
> Perlu berjalan terlebih agar app bisa mengakses mysql yg di jalankan docker.
>
> Untuk ifo lebih lanjut seputar cara menjalankan docker commpose baca file "Readme.Docker.md"
>
> sebelum menjalankan app plikasi pastikan sudah terdapat file `.env` dan letakan
> variable `SQLALCHEMY_DATABASE_URL=mysql+pymysql://root:password@localhost/MYDB`.
>
> sekarang dowenload semua dependendcy yg dibutuhkan dengan menjalankan commad
> `poetry install`. tetapi akan ada masalah ketika mendowenload dependendcy
> dimana versi paython active dari developer tidak sesuai. untuk mengatasi masalah itu,
> pastikan versi python yg sedang active sesuai
>
>
> setelah docker compose sudah berjalan dan environment sudah di setup. jalankan
> applikasi dengan `python run.py`
>
>

## How to develop the app ?

### first you need to understand the code structure first.

```bash
app\                    #app is the name of the application directory
    user\               #user is domain folder 
        user_models     #user_models is folder for defining the sape of entity.
        user_dto        #user_dto is folder of define object or `types`. 
        user_router     #user_router is folder of end_point code. 
        user_services   #user_service is folder of the business logic of user,
    utils\              #utils is please to store global entity code.  
         optional       #optiona is example of logic `Dewa wrote`
    libs\               #libs is folder contain an adapter logic of third party usage. 
        password_lib    #password_libs is module of password need's, like hashing and verifying it. 
        jwt_lib         #jwt_libs also module of jwt logic dependent third party. 
        sql_alchemy_lib #sql_alchemy_lib contain logic about connecting to database
    main
```

> - **app**: adalah directory utama untuk menyimpa semua logic applikasi
>
> - **user**: adalah sejenis domain folder. fungsinya untuk menimpan semua logic yg berkaitan
    > dengan user. seperti authentication atau membuat connection diantara user.
>
> - **user_models**: adalah folder yg berisi model database yg berkaitan denga user.
    > di saat membuat sebuah table, jika table tersebut akan memiliki bisini logic yg cukup padat.
    > buatlah folder tersendiri untuk itu.
>
> - **user_dto**: adalah folder untuk menyimpan data yg terdefinisi, tujuan utamnya untuk
    > menulis objek yg rapi utnuk di lakukan oprasi.
>
> - **user_router**: adalah folder untuk menyimpan end poin untuk di gunakan. saat menulis
    endpoint logic pastikan logic yg ditulis singkat dikarnkaan folder ini juga akan
    digunakan untuk kebutuhan documentations.
>
> - **user_service**: service folder adalah folder untuk menluis
    > bussiness logic dari domain, logic di sini bisa beruap penarikan
    > data, mutasi data dan pendaftaran data.
> - **utils**: is tempat untuk menyimp global logic.
>
> - **optiona**: adalah contoh global logic yg dewa tulis.
>
> - **libs** adalah folder yg berisi adaptor dari logic yg
    > mengunakan third party pada logicnya
>
> - **password_libs**: adalah module yg berisi logic untuk
    > menghashing password dan mengvalidasi hashing password.
>
> - **jwt_libs**: adalah module untuk mebuat jwt authentication service.
>
> - **sql_alchemy_lib**: adalah module untuk menyimpan logic yg
    > berkaintan dengan database


developer should a ware the different global module name and business module name. the business domain module wrote
without `sufix s` and global logic wrote with `sufix s`.

### disaat menulis logic, pastikan dependency yg digunaakan tersusun

rapi.

```python
# on the top write the python standard library module.
from typing import Type
# on the second part you need to wrote framework module will be needed. its might be a type use to annotate a variable or error to be raise, but please to make it as logic dependency, make logic dependency on libs folder
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
# on third part is module from same domain.
from .user_model import UserModel
from . import user_dtos
# on the last part is global module, it can be from utils ro libs
from app.libs import password_lib
from app.utils import optional
```

### membuat tabe pada database

> 1. buat database seuai bussnes domainnya.
> 2. import database tersebut pada fodlder `migrations/env.py.`
> 3. setelah mengimport table pada `migrations/env.py.`jalankan code
     > `alembic revision --autogenerate -m "<comit message>"`. then
     > run `alembic upgrade head`.

akan ada masalah di saat anda menjalankan comment migration.
masalah dapat di indentifikasi dengan terdapat error pada log
pada shell. atau disaat anda melihat isi folder terbaru pada
directory "migrations/versions" fungsi upgrade berisi pass

```python
## Contoh migration yg berhasi.
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', mysql.CHAR(length=36), nullable=False),
                    sa.Column('username', sa.String(length=50), nullable=True),
                    sa.Column('email', sa.String(length=50), nullable=True),
                    sa.Column('password', sa.String(length=100), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
```