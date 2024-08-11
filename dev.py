import os
import subprocess


def main():
    # subprocess.call(["fastapi", "dev", "app/main.py"])
    # os.environ["IS_TESTING"] = "False"
    os.system("fastapi dev app/main.py")


if __name__ == "__main__":
    main()
