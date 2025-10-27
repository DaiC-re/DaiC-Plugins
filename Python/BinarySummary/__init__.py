import DaiCCore
import requests
import sys
import os

class BinarySummary(DaiCCore.Plugin):
    """
    Analyzes binary imports using a SECURE local middleware.
    This plugin REQUIRES the 'DAIC_MIDDLEWARE_KEY' environment
    variable to be set.
    """
    
    name = "Binary Summary"
    description = "Analyzes binary imports via secure Claude middleware"
    version = "2.0.0"
    author = "DaiC Team"

    MIDDLEWARE_URL = "http://daic.re/ask-claude/analyze-binary/"
    
    def __init__(self):
        super().__init__()

    def init(self):
        self.middleware_key = os.environ.get("DAIC_MIDDLEWARE_KEY")

        if not self.middleware_key:
            print(f"[{self.name}] FATAL ERROR: 'DAIC_MIDDLEWARE_KEY' environment variable not set.", file=sys.stderr)
            print(f"[{self.name}] Please set this to the middleware's secret API key.", file=sys.stderr)
        else:
            print(f"[{self.name}] Plugin instantiated and key loaded.")
            print(f"[{self.name}] Middleware target: {self.MIDDLEWARE_URL}")

    def run(self):
        if not self.middleware_key:
            print(f"[{self.name}] Error: Middleware key not set. Cannot run analysis.", file=sys.stderr)
            return

        print(f"[{self.name}] Fetching binary imports...")
        try:
            imports = DaiCCore.get_imports()
        except Exception as e:
            print(f"[{self.name}] Error getting imports: {e}", file=sys.stderr)
            return

        imports_msg = ""
        for i in imports:
            offset = getattr(i, 'offset', 'N/A')
            file_name = getattr(i, 'file_name', 'N/A')
            func_name = getattr(i, 'fonction_name', 'N/A')
            imports_msg += f"{offset} {file_name} {func_name}\n"

        if not imports_msg.strip():
            print(f"[{self.name}] No imports to analyze.")
            return

        print(f"[{self.name}] Sending secure request to middleware...")
        
        payload = {
            "user_prompt": (
                "From the following list of imported functions... "
                "what is its likely purpose... " # (Your full prompt here)
                f"\n\n{imports_msg}"
            ),
            "model": "claude-opus-4-20250514"
        }
        
        headers = {
            "Authorization": f"Bearer {self.middleware_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(self.MIDDLEWARE_URL, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            response_text = data.get("response")

            self.print_formatted_response(response_text)

        except requests.exceptions.ConnectionError:
            print(f"[{self.name}] FATAL ERROR: Could not connect to middleware at {self.MIDDLEWARE_URL}", file=sys.stderr)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"[{self.name}] FATAL ERROR: 403 Forbidden. Your 'DAIC_MIDDLEWARE_KEY' is WRONG.", file=sys.stderr)
            elif e.response.status_code == 429:
                print(f"[{self.name}] ERROR: 429 Too Many Requests. You are being rate-limited.", file=sys.stderr)
            else:
                print(f"[{self.name}] Middleware returned an HTTP error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[{self.name}] An unexpected error occurred: {e}", file=sys.stderr)

    def terminate(self):
        print(f"[{self.name}] Terminated.")

    def print_formatted_response(self, response_text: str):
        print("=" * 60)
        print(f"CLAUDE AI RESPONSE ({self.name})")
        print("=" * 60)
        print(response_text or "No valid response text received.")
        print("\n" + "=" * 60)
        print("Response provided by local secure middleware.")
        print("=" * 60)
