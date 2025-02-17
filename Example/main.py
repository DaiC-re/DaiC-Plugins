import DaiCCore

def ai_generator():
    DaiCCore.add_to_menu("test")
    def print_test():
        print("test toolBar")
    DaiCCore.add_to_tool("test2", print_test)
    file = DaiCCore.get_file()
DaiCCore.register("AiDecompiler", "call decompiler model with llama_cpp", ai_generator)
a = DaiCCore.get_valid_list()
