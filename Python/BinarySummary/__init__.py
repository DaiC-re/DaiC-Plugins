import DaiCCore
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

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

    # MIDDLEWARE_URL = "https://daic.re/ask-claude/analyze-binary/"
    MIDDLEWARE_URL = "https://daic.re/ask-claude/analyze-binary"
    
    def init(self):
        self.middleware_key = os.environ.get("DAIC_MIDDLEWARE_KEY")

        if not self.middleware_key:
            # print(f"[{self.name}] FATAL ERROR: 'DAIC_MIDDLEWARE_KEY' environment variable not set.", file=sys.stderr)
            # print(f"[{self.name}] Please set this to the middleware's secret API key.", file=sys.stderr)
            raise AssertionError("FATAL ERROR: 'DAIC_MIDDLEWARE_KEY' environment variable not set.")
        else:
            self.log("Plugin instantiated and key loaded.")
            self.log(f"Middleware target: {self.MIDDLEWARE_URL}")

    def run(self):
        if not self.middleware_key:
            self.log("Error: Middleware key not set. Cannot run analysis.")
            return

        self.log("Fetching binary imports...")
        try:
            imports = DaiCCore.get_imports()
        except Exception as e:
            self.log(f"Error getting imports: {e}")
            return

        imports_msg = ""
        for i in imports:
            offset = getattr(i, 'offset', 'N/A')
            file_name = getattr(i, 'file_name', 'N/A')
            func_name = getattr(i, 'fonction_name', 'N/A')
            imports_msg += f"{offset} {file_name} {func_name}\n"

        if not imports_msg.strip():
            self.log("No imports to analyze.")
            return

        self.log("Sending secure request to middleware...")
        
        # user_prompt = (
        #     "From the following list of imported functions by a binary "
        #     "(formatted as: offset, file_name, function_name), "
        #     "can you please analyze them and provide information on this binary? "
        #     "Specifically, what is its likely purpose (e.g., utility, malware, system component), "
        #     "what are its key capabilities, and are there any suspicious imports?\n\n"
        #     f"{imports_msg}"
        # )
        #
        # system_prompt = (
        #     "You are an expert in reverse engineering and binary analysis. "
        #     "You provide clear, concise, and actionable insights based on import tables."
        # )
        #
        payload = {
            "imports": imports_msg,
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
            self.log(f"FATAL ERROR: Could not connect to middleware at {self.MIDDLEWARE_URL}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                self.log("FATAL ERROR: 403 Forbidden. Your 'DAIC_MIDDLEWARE_KEY' is WRONG.")
            elif e.response.status_code == 429:
                self.log("ERROR: 429 Too Many Requests. You are being rate-limited.")
            else:
                self.log(f"Middleware returned an HTTP error: {e}")
        except Exception as e:
            self.log(f"An unexpected error occurred: {e}")

    def terminate(self):
        self.log("Terminated.")

    def print_formatted_response(self, response_text: str):
        print("=" * 60)
        print(f"AI RESPONSE ({self.name})")
        print("=" * 60)
        print(response_text or "No valid response text received.")
        print("\n" + "=" * 60)
        print("End of the response.")
        print("=" * 60)

    def log(self, message):
        print(f"[{self.name}] {message}", file=sys.stderr)
