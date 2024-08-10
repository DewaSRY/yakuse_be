import os

import uvicorn

from app.main import app


def main():
    # subprocess.call(["fastapi", "dev", "app/main.py"])
    os.system("fastapi dev app/main.py")


if __name__ == "__main__":
    print("hallo wrld")
    os.environ["IS_TESTING"] = "True"
    main()
