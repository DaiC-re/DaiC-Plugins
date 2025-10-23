from openai import OpenAI
import DaiCCore

def ai_generator():
    base_url = DaiCCore.input_dialog("url")
    api_key = DaiCCore.input_dialog("api_key"),
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

    def completion():
        input = DaiCCore.input_dialog("Prompt:")
        completion = client.chat.completions.create(
            model="NousResearch/Meta-Llama-3-8B-Instruct",
            messages=[
                {"role": "user", "content": input}
                ]
            )
        output = output["choices"][0]["text"]
        DaiCCore.print_dialog(output, "Result: ")

    DaiCCore.add_to_tool("Completion", completion)

DaiCCore.register("AiApi", "Call distant llm model", ai_generator)
