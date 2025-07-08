import DaiCCore

def example():
    DaiCCore.add_to_menu("test")
    def print_test():
        print("test toolBar")
    DaiCCore.add_to_tool("test2", print_test)
    file = DaiCCore.get_file()
    print (file)
    imports = DaiCCore.get_imports()
    print(imports)


DaiCCore.register("Example", "Example plugin", example)
