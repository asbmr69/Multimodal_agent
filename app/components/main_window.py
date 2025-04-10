from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QStatusBar)
from PyQt6.QtCore import Qt

from .code_editor import CodeEditor
from .file_explorer import FileExplorer
from .chat_section import ChatSection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multimodal AI Agent")
        self.setMinimumSize(1200, 800)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Create splitter for resizable sections
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.splitter)
        
        # Left side - File Explorer
        self.file_explorer = FileExplorer()
        self.splitter.addWidget(self.file_explorer)
        
        # Middle - Code Editor
        self.code_editor = CodeEditor()
        self.splitter.addWidget(self.code_editor)
        
        # Right side - Chat Section
        self.chat_section = ChatSection()
        self.splitter.addWidget(self.chat_section)
        
        # Set initial sizes (10% file explorer, 60% code editor, 30% chat)
        self.splitter.setSizes([100, 700, 300])
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Connect signals
        self.file_explorer.file_selected.connect(self.open_file)
        
    def open_file(self, file_path):
        """Open a file in the code editor when selected in file explorer"""
        self.code_editor.set_file(file_path)
        self.status_bar.showMessage(f"Opened: {file_path}") 