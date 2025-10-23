import DaiCCore
from PySide6.QtWidgets import QDockWidget, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
import sys
import io

# --- Helper Class to Redirect Output ---
class QtStream(io.StringIO):
    """
    A simple stream class that redirects stdout/stderr to a QTextEdit widget.
    """
    def __init__(self, text_widget):
        super().__init__()
        self.widget = text_widget

    def write(self, text):
        """Writes text to the widget and ensures it's visible."""
        self.widget.insertPlainText(text)
        self.widget.ensureCursorVisible() # Auto-scroll to the bottom

# --- Custom QLineEdit with History ---
class HistoryLineEdit(QLineEdit):
    """
    A QLineEdit subclass that handles command history with Up/Down arrow keys.
    """
    def __init__(self, plugin, parent=None):
        super().__init__(parent)
        self.plugin = plugin # Store a reference to the main plugin instance

    def keyPressEvent(self, event: QKeyEvent):
        """Override to handle specific key presses."""
        if event.key() == Qt.Key.Key_Up:
            self.plugin.navigate_history_up()
        elif event.key() == Qt.Key.Key_Down:
            self.plugin.navigate_history_down()
        else:
            # For all other keys, use the default behavior
            super().keyPressEvent(event)


# --- The Main Plugin Class ---
class PythonInterpreter(DaiCCore.Plugin):
    """
    A plugin that loads a simple, interactive Python interpreter inside a QDockWidget.
    """
    # --- Plugin Metadata ---
    name = "Python Interpreter"
    description = "Adds a dockable Python interpreter widget with command history."
    version = "1.1.0"
    author = "Gemini & DaiC Team"

    def __init__(self):
        super().__init__()
        # --- Initialize Plugin State ---
        self.main_window = None
        self.dock_widget = None
        self.output_console = None
        self.input_line = None
        # Store execution context to preserve variables between commands
        self.interpreter_context = {}
        # Keep track of original streams to restore them on termination
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        # --- New members for command history ---
        self.command_history = []
        self.history_index = -1 # -1 indicates we are at the newest entry (not in history)

    def init(self):
        """
        Initializes the plugin and creates the UI elements.
        
        This method assumes your C++ host application calls it with a
        reference to the main QMainWindow instance.
        """
        self.main_window = DaiCCore.get_main_window()
        if not self.main_window:
            print(f"[{self.name}] Error: Main window instance was not provided.")
            return

        # 1. Create the main dock widget
        self.dock_widget = QDockWidget("Python Interpreter", self.main_window)
        self.dock_widget.setObjectName("PythonInterpreterDock")
        self.dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # 2. Create the central widget that will hold the interpreter UI
        interpreter_ui_widget = QWidget()
        layout = QVBoxLayout(interpreter_ui_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # 3. Create the output console (a read-only QTextEdit)
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setStyleSheet(
            "QTextEdit { background-color: #2E3440; color: #E5E9F0; font-family: 'Consolas', 'Courier New', monospace; }"
        )
        
        # 4. Create the input line using our new custom widget
        self.input_line = HistoryLineEdit(self) # Pass a reference to this plugin instance
        self.input_line.setStyleSheet(
            "QLineEdit { background-color: #3B4252; color: #E5E9F0; font-family: 'Consolas', 'Courier New', monospace; border: 1px solid #4C566A; }"
        )
        
        # 5. Assemble the layout
        layout.addWidget(self.output_console)
        layout.addWidget(self.input_line)
        self.dock_widget.setWidget(interpreter_ui_widget)

        # 6. Connect the input line's returnPressed signal to execute the command
        self.input_line.returnPressed.connect(self.execute_command)

        # 7. Add context to the interpreter's scope for interacting with the app
        self.interpreter_context['app_main_window'] = self.main_window
        self.interpreter_context['plugin'] = self
        self.interpreter_context['DaiCCore'] = DaiCCore # <-- MAKE DaiCCore AVAILABLE
        
        # 8. Dock the widget into the main window (bottom area by default)
        self.main_window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.dock_widget)
        
        print(f"[{self.name}] Initialized successfully!")

    def run(self):
        """
        Activates the plugin by showing the widget and redirecting output streams.
        """
        if not self.dock_widget:
            print(f"[{self.name}] Cannot run, plugin was not initialized correctly.")
            return

        # Make the dock widget visible
        self.dock_widget.show()
        
        # Redirect stdout and stderr to our custom QtStream
        qt_stream = QtStream(self.output_console)
        sys.stdout = qt_stream
        sys.stderr = qt_stream
        
        # Welcome message
        self.output_console.append(f"--- {self.name} v{self.version} ---\n")
        self.output_console.append("Access the main window via 'app_main_window' and core lib via 'DaiCCore'.\n")
        self.output_console.insertPlainText(">>> ")
        
        self.input_line.setFocus()

    def terminate(self):
        """
        Cleans up resources when the plugin is unloaded.
        """
        # Restore the original stdout and stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

        # Remove and delete the dock widget if it exists
        if self.dock_widget and self.main_window:
            self.main_window.removeDockWidget(self.dock_widget)
            self.dock_widget.deleteLater()
            self.dock_widget = None
        
        print(f"[{self.name}] Terminated cleanly.")

    def execute_command(self):
        """
        Takes text from the input line, executes it, and displays the result.
        """
        command = self.input_line.text().strip()
        
        # Add command to history if it's not empty and not a duplicate of the last one
        if command and (not self.command_history or self.command_history[-1] != command):
            self.command_history.append(command)
        self.history_index = len(self.command_history) # Reset history navigation

        if not command:
            self.output_console.insertPlainText("\n>>> ")
            return

        # Echo the command to the console
        self.output_console.insertPlainText(command + '\n')
        self.input_line.clear()
        
        try:
            # First, try to evaluate the command as an expression (e.g., "2 + 2")
            result = eval(command, self.interpreter_context)
            if result is not None:
                self.output_console.insertPlainText(repr(result) + '\n')
        except SyntaxError:
            # If it's not an expression, execute it as a statement (e.g., "x = 5")
            try:
                exec(command, self.interpreter_context)
            except Exception as e:
                self.output_console.insertPlainText(f"Error: {e}\n")
        except Exception as e:
            self.output_console.insertPlainText(f"Error: {e}\n")
        
        # Show the prompt for the next command
        self.output_console.insertPlainText(">>> ")

    def navigate_history_up(self):
        """Navigate to the previous command in history."""
        if not self.command_history:
            return
        # Move the index back, but not past the beginning of the list
        self.history_index = max(0, self.history_index - 1)
        self.input_line.setText(self.command_history[self.history_index])

    def navigate_history_down(self):
        """Navigate to the next command in history."""
        if not self.command_history:
            return
        # Move the index forward, but not past the end of the list
        self.history_index = min(len(self.command_history), self.history_index + 1)
        
        if self.history_index == len(self.command_history):
            # If we're at the end, clear the line to start a new command
            self.input_line.clear()
        else:
            self.input_line.setText(self.command_history[self.history_index])
