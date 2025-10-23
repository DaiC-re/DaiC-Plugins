import DaiCCore
from openai import OpenAI

def AiDecompile():
    server_addr = DaiCCore.get_str()
    client = OpenAI(base_url=f"http://{server_addr}/v1", api_key="dummy")
    def f(dissasm):
        before = f"# This is the assembly code:\n"
        after = "\n# What is the source code?\n"
        prompt = before+"""call		0x1dcb
push		0x45
mov		dword ptr [rbp - 0x4c], eax
call		0x1dcb
push		qword ptr [rbp - 0x44]
mov		dword ptr [rbp - 0xc], eax
mov		eax, dword ptr [rbp - 0x20]
mov		ecx, eax
mov		edi, eax
mov		esi, eax
and		ecx, 0xfff
sar		eax, 0x10
sar		esi, 0xc and		eax, 0xffff
mov		dword ptr [rbp - 0x50], ecx
and		edi, 0x8000
and		esi, 7
mov		dword ptr [rbp - 0x40], eax
call		0x4ebd
test		eax, eax
jne		0x123d
push		0x21
call		0x1dcb
lea		eax, [rbp + 8]
push		rax
push		0x4085d8
push		1
push		rbx
push		0x4085e8
"""+after
        resp = client.completions.create(
                model="LLM4Binary/llm4decompile-1.3b-v2",
                prompt=prompt
                )
        print(resp.choices[0].text)
    DaiCCore.connect_functions_table(f)

DaiCCore.register("AiDecompiler", "Decompile assembly code", AiDecompile)

