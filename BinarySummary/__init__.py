import DaiCCore
import anthropic

client = anthropic.Anthropic()

def print_formatted_response(response):
    """Pretty print Anthropic API response with formatting"""
    print("=" * 60)
    print("CLAUDE RESPONSE")
    print("=" * 60)
    
    for i, content_block in enumerate(response.content):
        if content_block.type == 'text':
            print(f"\nContent Block {i+1}:")
            print("-" * 40)
            print(content_block.text)
            print("-" * 40)
    
    print(f"\nModel: {response.model}")
    print(f"Stop Reason: {response.stop_reason}")
    print(f"Usage: {response.usage}")

def binaryAction():
    imports = DaiCCore.get_imports()
    imports_msg = ""
    for i in imports:
        imports_msg += f"{i.offset} {i.file_name} {i.fonction_name}\n"
    prompt = f"From the following list of imported function by a binary with the offset, file_name and function_name, can you give me information on this binary {imports_msg}"
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        temperature=1,
        system="You are an expert in reverse engineering",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    print(print_formatted_response(message))

DaiCCore.register("BinarySummary", "Get binary import and do some action", binaryAction)
