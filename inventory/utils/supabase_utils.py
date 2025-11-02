import os
from dotenv import load_dotenv
from supabase import create_client, Client

# ✅ Correct way to load environment variables
load_dotenv(r"C:\Users\EvenceMohauLanga\OneDrive - Net Nine Nine\Documents\Jacky\.env")

# ✅ Get credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials. Check your .env file.")

# ✅ Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Function to upload image to Supabase Storage
def upload_image(file_obj, bucket="images", path=""):
    """
    Uploads an image to Supabase Storage and returns its public URL.
    Args:
        file_obj: Django UploadedFile or file-like object
        bucket: Supabase storage bucket name
        path: optional folder path inside bucket
    """
    filename = file_obj.name
    storage_path = f"{path}/{filename}" if path else filename

    # ✅ Read file content safely
    file_bytes = file_obj.read()
    file_obj.seek(0)  # Reset pointer so Django can still use it if needed

    # ✅ Upload file to Supabase
    res = supabase.storage.from_(bucket).upload(storage_path, file_bytes)

    # ✅ Handle errors properly
    if isinstance(res, dict) and res.get("error"):
        raise ValueError(res["error"]["message"])

    # ✅ Get public URL
    public_url = supabase.storage.from_(bucket).get_public_url(storage_path)
    return public_url["publicUrl"] if isinstance(public_url, dict) else public_url

def insert_aux_relay_inventory(data: dict):
    """
    Inserts a new record into the aux_relay_inventory table.
    """
    try:
        res = supabase.table("aux_relay_inventory").insert(data).execute()
        
        # Check if there's an error in the response
        if hasattr(res, 'error') and res.error:
            raise ValueError(f"Supabase error: {res.error.message}")
            
        return res
    except Exception as e:
        print(f"Error inserting data: {e}")
        # Add more specific error handling here
        raise

# Usage example:
try:
    data = {
        "column1": "value1",
        "column2": "value2",
        # ... your data
    }
    result = insert_aux_relay_inventory(data)
    print("Insert successful:", result)
except Exception as e:
    print("Insert failed:", e)


