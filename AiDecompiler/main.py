from llama_cpp import Llama
import DaiCRegister

def ai_generator(bv):
    model_path=input("model path = ")
    llm = Llama(
          model_path,
          # n_gpu_layers=-1, # Uncomment to use GPU acceleration
          # seed=1337, # Uncomment to set a specific seed
          # n_ctx=2048, # Uncomment to increase the context window
    )
    output = llm(
          "Q: Name the planets in the solar system? A: ", # Prompt
          max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
          stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
          echo=True # Echo the prompt back in the output
    ) # Generate a completion, can also call create_completion
    print(output)

DaiCRegister.register(ai_generator)
