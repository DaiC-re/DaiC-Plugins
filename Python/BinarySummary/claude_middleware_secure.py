import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from anthropic import Anthropic, AnthropicError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# --- 1. Load Secrets and Configuration ---
# --- THIS IS THE FIX ---
# Find the directory this script lives in
BASE_DIR = Path(__file__).resolve().parent
# Load the .env file from that specific directory
load_dotenv(dotenv_path=BASE_DIR / ".env")  # <--- 2. MODIFY THIS LINE
# --- END OF FIX ---

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
DAIC_MIDDLEWARE_KEY = os.environ.get("DAIC_MIDDLEWARE_KEY")

if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in .env file")
if not DAIC_MIDDLEWARE_KEY:
    raise ValueError("DAIC_MIDDLEWARE_KEY not set in .env file")

# --- 2. Initialize App, Rate Limiter, and Security ---
limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

auth_scheme = HTTPBearer()

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def check_api_key(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    """
    This function is a dependency. FastAPI will run it on every
    request that requires it. It checks the Bearer token.
    """
    if not (creds and creds.credentials == DAIC_MIDDLEWARE_KEY):
        print(f"Invalid API key attempt from {get_remote_address}")
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return True

class BinaryAnalysisRequest(BaseModel):
    imports: str
    # model: str | None = "claude-opus-4-20250514"

# --- 5. New, Secure, Task-Specific Endpoint ---
@app.post("/analyze-binary")
@limiter.limit("4/minute")
async def analyze_binary(
    request: Request,
    body: BinaryAnalysisRequest,
    is_authenticated: bool = Depends(check_api_key) # This line enforces authentication
):
    """
    This endpoint is ONLY for binary analysis.
    The System Prompt is hardcoded and cannot be changed by the client.
    """
    print(f"Received /analyze-binary request from {get_remote_address(request)}")
    
    SYSTEM_PROMPT = (
        "You are an expert in reverse engineering and binary analysis. "
        "You provide clear, concise, and actionable insights based on import tables."
    )

    USER_PROMPT = (
        "From the following list of imported functions by a binary "
        "(formatted as: offset, file_name, function_name), "
        "can you please analyze them and provide information on this binary? "
        "Specifically, what is its likely purpose (e.g., utility, malware, system component), "
        "what are its key capabilities, and are there any suspicious imports?\n\n"
        f"{body.imports}"
    )
    
    try:
        message = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": USER_PROMPT}
            ]
        )
        
        if message.content:
            return {"response": message.content[0].text.strip()}
        else:
            raise HTTPException(status_code=500, detail="Invalid API response")

    except AnthropicError as e:
        print(f"Anthropic API error: {e}")
        raise HTTPException(status_code=500, detail=f"Anthropic API Error: {e.message}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Secure Claude Middleware is running."}
