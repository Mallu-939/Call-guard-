import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI(title="Call Guard API")

# Initialize Supabase client using environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class CallCheckRequest(BaseModel):
    phone_number: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "Call Guard API"}

@app.post("/check-number")
def check_number(request: CallCheckRequest):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase credentials not configured")
    
    # Query your Supabase table (assumes a table named 'spam_numbers' with a 'phone_number' column)
    response = supabase.table("spam_numbers").select("*").eq("phone_number", request.phone_number).execute()
    
    if response.data:
        return {"phone_number": request.phone_number, "is_spam": True, "details": response.data[0]}
    
    return {"phone_number": request.phone_number, "is_spam": False}
