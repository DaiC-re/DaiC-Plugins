from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import DaiCCore
import time

# Worker that runs in a separate thread
class Worker(QObject):
    finished = Signal(str)

    @Slot()
    def run(self):
        # Simulate long task
        time.sleep(2)
        self.finished.emit("Worker done!")

# Plugin widget with thread-based logic
class MyPluginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threaded Plugin")

        self.label = QLabel("Click to start thread")
        self.button = QPushButton("Start Worker")

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.start_thread)

    def start_thread(self):
        self.worker = Worker()
        self.thread = QThread()

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_worker_done)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_worker_done(self, result):
        self.label.setText(result)

def runner():
    plugin = MyPluginWidget()
    DaiCCore.dock_widget(plugin)

DaiCCore.register("QThreadTest", "QThread test", runner)
