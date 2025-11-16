import uvicorn
from dotenv import load_dotenv  # <-- Import karo
import os                     # <-- Import karo

load_dotenv() # Taaki .env se PORT bhi le sake (agar set kiya toh)

# Render 'PORT' naam ka variable set karta hai
# Local ke liye default 8000
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app",
        # Host ko 0.0.0.0 rehne do deployment ke liye
        host="0.0.0.0", 
        port=PORT,
        reload=True
    )