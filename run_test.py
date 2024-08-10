import os
import uvicorn

from app.main import app
from app.libs import sql_alchemy_lib


def main():
    # Drope all table first
    sql_alchemy_lib.Base \
        .metadata.drop_all(bind=sql_alchemy_lib.engine)
    # Create new table thne
    sql_alchemy_lib.Base \
        .metadata.create_all(bind=sql_alchemy_lib.engine)

    # subprocess.call(["fastapi", "dev", "app/main.py"])

    os.system("pytest")


if __name__ == "__main__":
    os.environ["IS_TESTING"] = "True"
    main()
