from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

if __name__ == "__main__":
    print("----------------------------------------")
    print("Server starting... Available routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule}")
    print("----------------------------------------")
    
    # Disable auto-reloader but keep debug mode
    app.run(
        host="127.0.0.1", 
        port=5000, 
        debug=True,
        use_reloader=False  # Disable auto-reloader
    )
