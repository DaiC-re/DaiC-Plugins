from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
import os

max_model_len, tp_size = 8192, 1
# model_name = "deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct"
model_dir = os.path.expanduser('~/deepseek-coder-1.3b-instruct')
tokenizer = AutoTokenizer.from_pretrained(model_dir)
llm = LLM(model=model_dir, tensor_parallel_size=tp_size, max_model_len=max_model_len, trust_remote_code=True, enforce_eager=True)
sampling_params = SamplingParams(temperature=0.3, max_tokens=256, stop_token_ids=[tokenizer.eos_token_id])

messages_list = [
    [{"role": "user", "content": "Who are you?"}],
    [{"role": "user", "content": "write a quick sort algorithm in python."}],
    [{"role": "user", "content": "Write a piece of quicksort code in C++."}],
]

prompt_token_ids = [tokenizer.apply_chat_template(messages, add_generation_prompt=True) for messages in messages_list]

outputs = llm.generate(prompt_token_ids=prompt_token_ids, sampling_params=sampling_params)

generated_text = [output.outputs[0].text for output in outputs]
print(generated_text)

# def ai_generator():
#     model_path = DaiCCore.get_file()
#     llm = Llama(
#           model_path,
#           verbose=True
#           # n_gpu_layers=-1, # Uncomment to use GPU acceleration
#           # seed=1337, # Uncomment to set a specific seed
#           # n_ctx=2048, # Uncomment to increase the context window
#     )
#     def completion():
#         input = DaiCCore.input_dialog("Prompt:")
#         # input = llm.tokenize(input)
#         messages = [
#             { 'role': 'user', 'content': input }
#         ]
#         output = llm.create_chat_completion(messages)
#         # output = llm(
#         #         input,
#         #       max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
#         #       stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
#         #       # echo=True # Echo the prompt back in the output
#         # ) # Generate a completion, can also call create_completion
#         print(output)
#         output = output["choices"][0]["text"]
#         DaiCCore.print_markdown_dialog(output, "Result: ")
#     DaiCCore.add_to_tool("Chat", completion)
#
# DaiCCore.register("AiDecompiler", "Call decompiler model with llama_cpp", ai_generator)
