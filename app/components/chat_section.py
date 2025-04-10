from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLineEdit, 
                              QPushButton, QHBoxLayout, QLabel, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QTextCursor
from agents.agent_utils.agent_utils import AgentManager

class ChatMessage(QWidget):
    def __init__(self, text, is_user=True, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        # Sender label
        sender = "You" if is_user else "AI Agent"
        self.sender_label = QLabel(sender)
        self.sender_label.setStyleSheet(
            f"color: {'#2979FF' if is_user else '#00C853'}; font-weight: bold;"
        )
        self.layout.addWidget(self.sender_label)
        
        # Message text
        self.message = QTextEdit()
        self.message.setReadOnly(True)
        self.message.setPlainText(text)
        self.message.setFixedHeight(max(80, min(200, 20 * text.count('\n') + 60)))
        self.message.setStyleSheet(
            f"background-color: {'#E3F2FD' if is_user else '#F1F8E9'}; border-radius: 5px;"
        )
        self.layout.addWidget(self.message)


class ChatSection(QWidget):
    send_message_signal = pyqtSignal(str, str)  # Message and agent type
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Initialize agent manager
        self.agent_manager = AgentManager()
        
        # Header with title
        self.header = QHBoxLayout()
        self.title = QLabel("AI Agent Chat")
        self.title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.header.addWidget(self.title)
        
        # Agent selector
        self.agent_selector = QComboBox()
        self.agent_selector.addItems(["Coder Agent", "Assistant Agent"])
        self.header.addWidget(self.agent_selector)
        
        self.layout.addLayout(self.header)
        
        # Chat message area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.chat_container)
        self.layout.addWidget(self.scroll_area)
        
        # Input area
        self.input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.message_input)
        
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        
        self.assistant_button = QPushButton("Ask Assistant")
        self.assistant_button.clicked.connect(self.ask_assistant)
        self.assistant_button.setStyleSheet("background-color: #00C853; color: white;")
        self.input_layout.addWidget(self.assistant_button)
        
        self.layout.addLayout(self.input_layout)
        
        # Connect signals to handle messages
        self.send_message_signal.connect(self.receive_ai_response)
        
        # Add welcome message
        self.add_ai_message("Welcome! I'm your AI assistant. How can I help you today?")
        
    def send_message(self):
        """Send a user message"""
        message = self.message_input.text().strip()
        if not message:
            return
            
        # Add user message to chat
        self.add_user_message(message)
        
        # Clear input field
        self.message_input.clear()
        
        # Send to AI agent for response
        agent_type = self.agent_selector.currentText()
        self.send_message_signal.emit(message, agent_type)
        
        # Get response from the agent manager
        response = self.agent_manager.get_response(message, agent_type)
        self.add_ai_message(response)
        
    def ask_assistant(self):
        """Switch to Assistant Agent and prompt for message"""
        self.agent_selector.setCurrentText("Assistant Agent")
        self.message_input.setFocus()
        self.message_input.setPlaceholderText("Ask the Assistant Agent...")
        
    def add_user_message(self, text):
        """Add a user message to the chat"""
        message_widget = ChatMessage(text, is_user=True)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
        
    def add_ai_message(self, text):
        """Add an AI message to the chat"""
        message_widget = ChatMessage(text, is_user=False)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
        
    def receive_ai_response(self, message, agent_type):
        """Handle AI response (connected to AgentManager)"""
        # This will be used for asynchronous responses if needed
        pass
        
    def scroll_to_bottom(self):
        """Scroll chat to the bottom to show latest messages"""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ) 