from llama_cpp import Llama
import DaiCCore

def ai_generator():
    model_path = DaiCCore.get_file()
    llm = Llama(
          model_path,
          verbose=True
          # n_gpu_layers=-1, # Uncomment to use GPU acceleration
          # seed=1337, # Uncomment to set a specific seed
          # n_ctx=2048, # Uncomment to increase the context window
    )
    def completion():
        input = DaiCCore.input_dialog("Prompt:")
        # input = llm.tokenize(input)
        messages = [
            { 'role': 'user', 'content': input }
        ]
        output = llm.create_chat_completion(messages)
        # output = llm(
        #         input,
        #       max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
        #       stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
        #       # echo=True # Echo the prompt back in the output
        # ) # Generate a completion, can also call create_completion
        print(output)
        output = output["choices"][0]["text"]
        DaiCCore.print_markdown_dialog(output, "Result: ")
    DaiCCore.add_to_tool("Chat", completion)

DaiCCore.register("AiDecompiler", "Call decompiler model with llama_cpp", ai_generator)
