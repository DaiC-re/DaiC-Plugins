import DaiCCore  # this is your pybind11 module that exposes Plugin

class Example(DaiCCore.Plugin):
    name = "InfoPrinter"
    description = "A plugin that prints all its metadata and current path"
    version = "1.0.0"
    author = "DaiC Team"

    def init(self):
        print(f"[{self.name}] Initialized successfully!")

    def run(self):
        print("--- Plugin Information ---")
        print(f"Name:        {self.name}")
        print(f"Version:     {self.version}")
        print(f"Description: {self.description}")
        print(f"Author:      {getattr(self, 'author', 'Unknown')}")
        print(f"Path:        {__file__}")
        print("---------------------------")

    def terminate(self):
        print(f"[{self.name}] Terminated cleanly.")
