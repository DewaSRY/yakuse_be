from app.libs.supabase_client import supabase
from fastapi import UploadFile
import uuid

async def upload_image_to_supabase(file: UploadFile, bucket_name: str):
    try:
        # Baca isi file
        file_content = await file.read()

        # Buat nama file yang unik untuk mencegah duplikasi
        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        # Menyimpan file ke storage Supabase
        upload_response = supabase.storage.from_(bucket_name).upload(unique_filename, file_content)
        
        # Pastikan respons adalah dictionary dan cek apakah ada kunci 'error'
        if isinstance(upload_response, dict) and 'error' in upload_response:
            raise Exception(f"Error uploading file: {upload_response['error'].get('message', 'Unknown error')}")

        # URL publik file yang diupload
        public_url_response = supabase.storage.from_(bucket_name).get_public_url(unique_filename)

        # URL publik biasanya berupa string langsung
        if isinstance(public_url_response, str):
            public_url = public_url_response
        else:
            raise Exception("Unexpected response format when getting public URL")

        return public_url

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


