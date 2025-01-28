import os
import uvicorn
from pyngrok import ngrok
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Configure ngrok (for local development)
    ngrok_auth_token = os.environ.get("NGROK_AUTH_TOKEN")
    if ngrok_auth_token:
        ngrok.set_auth_token(ngrok_auth_token)
        public_url = ngrok.connect(8000).public_url
        print(f"ngrok tunnel created at: {public_url}")
        print(f"Public URL for your API: {public_url}")

    # Start the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)