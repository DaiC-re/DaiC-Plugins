from PySide6.QtCore import QMetaObject, Qt, QCoreApplication
import DaiCCore
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QComboBox, QApplication
)
from llama_cpp import Llama
import asyncio

class BackendSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select LLM Backend")

        # Layout
        layout = QVBoxLayout(self)

        # Label
        label = QLabel("Choose the backend to run your LLM model:")
        layout.addWidget(label)

        # ComboBox
        self.combo = QComboBox()
        self.combo.addItems(["llama_cpp", "vllm", "ollama", "openai_api"])
        layout.addWidget(self.combo)

        # OK / Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def selected_backend(self):
        return self.combo.currentText()


def llama_cpp_backend():
    model_path = DaiCCore.get_file()
    llm = Llama(
          model_path,
          verbose=True
          # n_gpu_layers=-1, # Uncomment to use GPU acceleration
          # seed=1337, # Uncomment to set a specific seed
          # n_ctx=2048, # Uncomment to increase the context window
    )
    async def completion():
        input = DaiCCore.input_dialog("Prompt:")
        # input = llm.tokenize(input)
        messages = [
            { 'role': 'user', 'content': input }
        ]
        async def create_output():
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
        await create_output()
    DaiCCore.add_to_tool("Chat", lambda: asyncio.run(completion()))

dialog = BackendSelectorDialog()

def AiDaic():
    # def create():
    #     widget = BackendSelectorDialog()
    #     DaiCCore.show_dialog(widget, "My Plugin UI")
    
    dialog.exec()

    # Ensure creation runs on main thread
    # QMetaObject.invokeMethod(QCoreApplication.instance(), create, Qt.QueuedConnection)
    # DaiCCore.exec_dialog(dialog)
    # dialog.exec()
    # backend = dialog.selected_backend()
    # print(f"Using {backend} backend")
    # if (backend == "llama_cpp"):
    #     pass
    # model_path = DaiCCore.get_file()
    # llama_cpp_backend()

    # match backend:
    #     case "llama_cpp":
    #         launch 


DaiCCore.register("AiDaiC", "Load multiple backend for decompilate", AiDaic)
