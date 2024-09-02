import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Muat variabel lingkungan dari .env
load_dotenv()

# Ganti dengan URL proyek dan kunci API Supabase Anda
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
