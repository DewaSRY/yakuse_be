"""
This file use to run app on production
"""

import os

import uvicorn

from app.main import app

if __name__ == "__main__":
    config = uvicorn.Config(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info")
    server = uvicorn.Server(config)
    server.run()
# if __name__ == "__main__":
#     TEXT = """
#     hallo
#     apakabar
#      kalian semua
#     """
#     TEXT_LIST = re.split("\\s{4,}", TEXT)
#
#     print(len(TEXT_LIST))
#     for s in TEXT_LIST:
#         print(s)
