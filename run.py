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
