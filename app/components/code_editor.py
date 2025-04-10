from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QComboBox, QPlainTextEdit)
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter
from PyQt6.QtCore import Qt, QRegularExpression

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            "\\bclass\\b", "\\bdef\\b", "\\bfor\\b", "\\bif\\b", "\\belif\\b", "\\belse\\b",
            "\\bwhile\\b", "\\btry\\b", "\\bexcept\\b", "\\bfinally\\b", "\\breturn\\b",
            "\\byield\\b", "\\bimport\\b", "\\bfrom\\b", "\\bas\\b", "\\bwith\\b",
            "\\bTrue\\b", "\\bFalse\\b", "\\bNone\\b", "\\blambda\\b"
        ]
        
        for pattern in keywords:
            self.highlighting_rules.append((QRegularExpression(pattern), keyword_format))
            
        # Function format
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#DCDCAA"))
        self.highlighting_rules.append(
            (QRegularExpression("\\b[A-Za-z0-9_]+(?=\\()"), function_format)
        )
        
        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append(
            (QRegularExpression("\".*\""), string_format)
        )
        self.highlighting_rules.append(
            (QRegularExpression("'.*'"), string_format)
        )
        
        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.highlighting_rules.append(
            (QRegularExpression("#.*"), comment_format)
        )
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


class CodeEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Toolbar layout
        self.toolbar = QHBoxLayout()
        
        # File name label
        self.file_label = QLabel("No file open")
        self.toolbar.addWidget(self.file_label)
        
        # Language selector
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Python", "JavaScript", "HTML", "CSS", "Text"])
        self.language_selector.setCurrentText("Python")
        self.toolbar.addWidget(self.language_selector)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        self.toolbar.addWidget(self.save_button)
        
        self.layout.addLayout(self.toolbar)
        
        # Text editor
        self.editor = QPlainTextEdit()
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        font = QFont("Consolas", 11)
        self.editor.setFont(font)
        self.layout.addWidget(self.editor)
        
        # Apply syntax highlighting
        self.highlighter = SyntaxHighlighter(self.editor.document())
        
        # Current file path
        self.current_file = None
        
    def set_file(self, file_path):
        """Open and display a file in the editor"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.editor.setPlainText(content)
            self.current_file = file_path
            self.file_label.setText(file_path.split('/')[-1])
        except Exception as e:
            self.file_label.setText(f"Error opening file: {str(e)}")
            
    def save_file(self):
        """Save the current file"""
        if not self.current_file:
            return
            
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            self.file_label.setText(f"Saved: {self.current_file.split('/')[-1]}")
        except Exception as e:
            self.file_label.setText(f"Error saving file: {str(e)}") 