import DaiCCore
from openai import OpenAI

def AiDecompile():
    server_addr = DaiCCore.get_str()
    client = OpenAI(base_url=f"http://{server_addr}/v1", api_key="dummy")
    def f(dissasm):
        before = f"# This is the assembly code:\n"
        after = "\n# What is the source code?\n"
        prompt = before+dissasm+after
        resp = client.completions.create(
                model="LLM4Binary/llm4decompile-9b-v2",
                prompt=prompt
                )
        print(resp.choices[0].text)
    DaiCCore.connect_functions_table(f)

DaiCCore.register("AiDecompiler", "Decompile assembly code", AiDecompile)
