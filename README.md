# Yasuke Be

## What is the app about ?

...

## How to run the app ?

> if you are in development and already running docker compose file (_read how on README.Docker.md_),make `.env` file
> and put this variable on it `SQLALCHEMY_DATABASE_URL=mysql+pymysql://root:password@localhost/MYDB`. when you make the
> file and
> already wrote the variable on it please make sure to not put spase on it.
>

1. first you need to install all dependency on poetry, so you need to run `poetry install --no-root`.Before downloading
   the app, please make sure your python version is correct and mathc with the version wrote on `project.toml` file.
2. after your docker is running and the dependency already installed. run `python run.py` on your shell. it will running
   the app on development mode.

> if you are in development mode to run the api just run `python dev.py` on your shall. please make sure your command
> line are in root directory

## How to develop the app ?

1. first you need to understand the code structure first.

```bash
app\                    #app is the name of the application directory, we use it to organize the main code and prevent other possibility when there is a need to have another grouping file for several needs.
    user\               #user is domain folder, it use for store business logic about on user domain. code every business logic on their own domain is good practice, its will make the app easy to document and debug
        user_models     #user_models is folder for defining the sape of entity. on this case the user_model use to define user table on database. if you are wont to make new table, event it's still about user business please think to make its on it's separate domain.
        user_dto        #user_dto is folder of define object or `types`. it's necessary to reduce complexity of business logic, so the code we build will more declarative, because the parameter and return value have they own unique name. 
        user_router     #user_router is folder of end_point code. its works like dore to access business logic. while writing router please make sure the code is have clean *hard code logic*, the code on router need to be clean because it's will work as document for developer, we also put swagger code on it, so it's need to have less hard logic. 
        user_services   #user_service is folder of the business logic of user, it the please we put hard business logic, like query database, inserting database, handle error joining table, make a shape of object use dto object, and many other. on tis file it's oke to wrote intimidate code logic, but if its possible please wrote declarative code, the code hwo reusable and easy to test.  
    utils\              #utils is please to store global entity code. it's will store the helper code will use every where on code base. the code wrote on this filee is an original code wrote by developer and clean from third party so make sure its easy to debug, understand, test and use. 
         optional       #optiona is example of logic `Dewa wrote` the file content logic to handle uncertainty of value, which its only use as return value. the optional object will store data value and en error value. so the logic will more easy to use.
    libs\               #libs is folder contain an adapter logic of third party usage. it's necessary to make separate logic to use outside library, so the developer only focus on what they wont to use.  
        password_lib    #password_libs is module of password need's, like hashing and verifying it. it's need to be separate because its dependent with third party and developer only need to focus on the purpose of use the code
        jwt_lib         #jwt_libs also module of jwt logic dependent third party. i build it as package ("a folder of module, every folder contain `__init__` file is count as package on python"). its build as package because the logic need to jwt business is quite complex. so if the code is sound confusing you can ask `Dewa for it`
        sql_alchemy_lib #sql_alchemy_lib contain logic about connecting to database, `dewa` wrote several comment on the file so please read it. developer will use this module alot so make sure  developer understand how to use it.
    main
```

developer should a ware the different global module name and business module name. the business domain module wrote
without `sufix s` and global logic wrote with `sufix s`.

2. to writing logic, you need to write the dependency on the top, and make sure its organize.

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

3. to define new table, developer need to run alambic command line after it

> 1. After define a table, developer should go to `migrations/env.py` file to import the table there.it's necessary so
     the alembic will know the table developer create is exist.
> 2. After define new table please run `alembic revision --autogenerate -m "<comit message>"`. then
     run `alembic upgrade head`.

