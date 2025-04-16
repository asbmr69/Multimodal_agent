from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QLineEdit, 
                              QPushButton, QHBoxLayout, QLabel, QComboBox, QScrollArea,
                              QSplitter, QFrame, QToolButton, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QTextCursor, QIcon, QPalette, QPixmap
from agents.assistant.assistant_agent import AssistantAgent
from agents.coder.coder_agent import create_main_flow, coding_agent_flow
import markdown
import os
import time
from datetime import datetime

class ChatMessage(QWidget):
    def __init__(self, text, is_user=True, agent_type=None, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(5)
        
        # Main message container with avatar and content
        message_container = QHBoxLayout()
        
        # Avatar section
        avatar_container = QWidget()
        avatar_container.setFixedSize(36, 36)
        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create avatar based on sender
        avatar_label = QLabel()
        avatar_label.setFixedSize(32, 32)
        avatar_label.setScaledContents(True)
        
        # Set appropriate avatar icon
        if is_user:
            avatar_path = os.path.join("resources", "user_avatar.svg")
            avatar_color = "#2979FF"
            sender = "You"
        else:
            if "Coder" in str(agent_type):
                avatar_path = os.path.join("resources", "coder_avatar.svg")
                avatar_color = "#FF5722"
                sender = "Coder Agent"
            else:
                avatar_path = os.path.join("resources", "ai_avatar.svg")
                avatar_color = "#00C853"
                sender = agent_type if agent_type else "AI Agent"
        
        # Apply avatar if file exists
        if os.path.exists(avatar_path):
            avatar_pixmap = QPixmap(avatar_path)
            avatar_label.setPixmap(avatar_pixmap)
        else:
            # Fallback to colored circle with initials
            avatar_label.setStyleSheet(
                f"background-color: {avatar_color}; border-radius: 16px; color: black; "
                f"font-weight: bold; font-size: 14px; text-align: center;"
            )
            avatar_label.setText(sender[0])
            avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        avatar_layout.addWidget(avatar_label, 0, Qt.AlignmentFlag.AlignTop)
        message_container.addWidget(avatar_container, 0, Qt.AlignmentFlag.AlignTop)
        
        # Message content container
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(5, 0, 5, 0)
        content_layout.setSpacing(3)
        
        # Header with sender info and timestamp
        header_layout = QHBoxLayout()
        
        # Sender label
        self.sender_label = QLabel(sender)
        self.sender_label.setStyleSheet(
            f"color: {avatar_color}; font-weight: bold; font-size: 13px;"
        )
        header_layout.addWidget(self.sender_label)
        
        # Add timestamp
        timestamp = QLabel(datetime.now().strftime("%I:%M %p"))
        timestamp.setStyleSheet("color: #9E9E9E; font-size: 11px;")
        header_layout.addStretch()
        header_layout.addWidget(timestamp)
        
        content_layout.addLayout(header_layout)
        
        # Message bubble with improved styling
        message_bubble = QWidget()
        bubble_layout = QVBoxLayout(message_bubble)
        bubble_layout.setContentsMargins(10, 10, 10, 10)
        
        # Message text - use QTextEdit with HTML support for markdown rendering
        self.message = QTextEdit()
        self.message.setReadOnly(True)
        self.message.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.message.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # If the message contains markdown code blocks or formatting, render it
        if not is_user and ("```" in text or "#" in text or "*" in text):
            # Convert markdown to HTML with syntax highlighting
            html_content = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
            self.message.setHtml(html_content)
            
            # Add custom CSS for code blocks
            self.message.document().setDefaultStyleSheet(
                "pre { background-color: #282c34; color: #abb2bf; padding: 10px; border-radius: 5px; }"
                "code { font-family: 'Consolas', 'Courier New', monospace; }"
                ".codehilite { background-color: #282c34; color: #abb2bf; padding: 10px; border-radius: 5px; }"
                ".codehilite .k { color: #c678dd; } /* Keyword */"
                ".codehilite .s { color: #98c379; } /* String */"
                ".codehilite .c1 { color: #5c6370; font-style: italic; } /* Comment */"
                ".codehilite .n { color: #e06c75; } /* Name */"
                ".codehilite .o { color: #56b6c2; } /* Operator */"
            )
        else:
            self.message.setPlainText(text)
        
        # Adjust height based on content
        line_count = text.count('\n') + 1
        self.message.setMinimumHeight(min(80, 20 * line_count))
        self.message.setMaximumHeight(max(80, min(400, 20 * line_count + 40)))
        
        # Style the message bubble based on sender
        if is_user:
            message_bubble.setStyleSheet(
                "background-color: #E3F2FD; border-radius: 12px; border-top-left-radius: 4px;"
            )
            self.message.setStyleSheet(
                "QTextEdit { background-color: transparent; border: none; color: #333333; }"
                "QScrollBar:vertical { width: 8px; background: transparent; }"
                "QScrollBar::handle:vertical { background: #BDBDBD; border-radius: 4px; }"
                "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }"
            )
        else:
            if "Assistant" in str(agent_type):
                message_bubble.setStyleSheet(
                    "background-color: #F1F8E9; border-radius: 12px; border-top-right-radius: 4px;"
                )
            else:  # Coder Agent
                message_bubble.setStyleSheet(
                    "background-color: #FFF3E0; border-radius: 12px; border-top-right-radius: 4px;"
                )
            self.message.setStyleSheet(
                "QTextEdit { background-color: transparent; border: none; color: #333333; }"
                "QScrollBar:vertical { width: 8px; background: transparent; }"
                "QScrollBar::handle:vertical { background: #BDBDBD; border-radius: 4px; }"
                "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }"
            )
        
        bubble_layout.addWidget(self.message)
        content_layout.addWidget(message_bubble)
        
        # Add the content container to the message container
        message_container.addWidget(content_container, 1)
        
        # Add the complete message container to the main layout
        self.layout.addLayout(message_container)
        
        # Add spacing instead of a line
        self.layout.addSpacing(10)


class ChatSection(QWidget):
    send_message_signal = pyqtSignal(str, str)  # Message and agent type
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Set background color for the entire chat section
        self.setStyleSheet("background-color: #F5F5F5;")
        
        # Initialize assistant agent
        self.assistant_agent = AssistantAgent()
        
        # Header with title and controls
        header_container = QWidget()
        header_container.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        header_container.setMinimumHeight(40)
        self.header = QHBoxLayout(header_container)
        self.header.setContentsMargins(20, 10, 20, 10)
        
        # Title with icon
        title_layout = QHBoxLayout()
        self.title = QLabel("Agent interface")
        self.title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.title.setStyleSheet("color: #424242;")
        title_layout.addWidget(self.title)
        self.header.addLayout(title_layout)
        
        # Add spacer
        self.header.addStretch()
        
        # Clear chat button
        self.clear_button = QToolButton()
        self.clear_button.setToolTip("Clear chat")
        clear_icon_path = os.path.join("resources", "clear_icon.svg")
        if os.path.exists(clear_icon_path):
            self.clear_button.setIcon(QIcon(clear_icon_path))
        else:
            self.clear_button.setText("Clear")
        self.clear_button.setIconSize(QSize(20, 20))
        self.clear_button.setStyleSheet(
            "QToolButton { border: none; padding: 5px; }"
            "QToolButton:hover { background-color: #F5F5F5; border-radius: 4px; }"
        )
        self.clear_button.clicked.connect(self.clear_chat)
        self.header.addWidget(self.clear_button)
        
        # Agent selection buttons
        self.assistant_button = QPushButton("Assistant")
        self.assistant_button.setMinimumWidth(100)
        self.assistant_button.setMinimumHeight(36)
        self.assistant_button.setStyleSheet(
            "QPushButton { padding: 5px 10px; border: 1px solid #E0E0E0; border-radius: 4px; background-color: #FFFFFF; color: #424242; }"
            "QPushButton:hover { background-color: #F5F5F5; color: #2979FF; }"
            "QPushButton:checked { background-color: #E3F2FD; border-color: #2979FF; color: #2979FF; }"
        )
        self.assistant_button.setCheckable(True)
        self.assistant_button.setChecked(True)
        self.assistant_button.clicked.connect(self.ask_assistant)
        self.header.addWidget(self.assistant_button)
        
        self.coder_button = QPushButton("Coder")
        self.coder_button.setMinimumWidth(100)
        self.coder_button.setMinimumHeight(36)
        self.coder_button.setStyleSheet(
            "QPushButton { padding: 5px 10px; border: 1px solid #E0E0E0; border-radius: 4px; background-color: #FFFFFF; color: #424242; }"
            "QPushButton:hover { background-color: #F5F5F5; color: #FF5722; }"
            "QPushButton:checked { background-color: #FFF3E0; border-color: #FF5722; color: #FF5722; }"
        )
        self.coder_button.setCheckable(True)
        self.coder_button.clicked.connect(self.ask_coder)
        self.header.addWidget(self.coder_button)
        
        self.layout.addWidget(header_container)
        
        # Chat message area with improved styling
        chat_area_container = QWidget()
        chat_area_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chat_area_layout = QVBoxLayout(chat_area_container)
        chat_area_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(
            "QScrollArea { border: none; background-color: #F5F5F5; }"
            "QScrollBar:vertical { width: 8px; background: transparent; margin: 0px; }"
            "QScrollBar::handle:vertical { background: #BDBDBD; border-radius: 4px; min-height: 30px; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }"
            "QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }"
        )
        
        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #F5F5F5;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(8)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)
        
        self.scroll_area.setWidget(self.chat_container)
        chat_area_layout.addWidget(self.scroll_area)
        
        self.layout.addWidget(chat_area_container, 1)  # Give it a stretch factor of 1
        
        # Input area with improved styling
        input_container = QWidget()
        input_container.setStyleSheet("background-color: #FFFFFF; border-top: 1px solid #E0E0E0;")
        input_container.setMinimumHeight(70)
        input_layout_container = QVBoxLayout(input_container)
        input_layout_container.setContentsMargins(20, 15, 20, 15)
        
        self.input_layout = QHBoxLayout()
        self.input_layout.setSpacing(10)
        
        # Message input with placeholder and styling
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.setMinimumHeight(40)
        self.message_input.setStyleSheet(
            "QLineEdit { padding: 8px 15px; border: 1px solid #E0E0E0; border-radius: 20px; background-color: #F5F5F5; color: #333333; }"
            "QLineEdit:focus { border: 1px solid #2979FF; background-color: #FFFFFF; color: #333333; }"
        )
        self.message_input.returnPressed.connect(self.send_message)
        self.input_layout.addWidget(self.message_input, 1)  # Give it a stretch factor of 1
        
        # Microphone button for audio/visual interaction
        self.mic_button = QPushButton()
        self.mic_button.setToolTip("Start audio/visual interaction")
        self.mic_button.setFixedSize(40, 40)
        self.mic_button.setText("🎤")
        self.mic_button.setStyleSheet(
            "QPushButton { background-color: #00C853; color: white; border-radius: 20px; }"
            "QPushButton:hover { background-color: #00E676; }"
            "QPushButton:checked { background-color: #FF5252; }"
        )
        self.mic_button.setCheckable(True)
        self.mic_button.clicked.connect(self.toggle_audio_visual_mode)
        self.input_layout.addWidget(self.mic_button)
        
        # Volume indicator (hidden by default)
        self.volume_indicator = QLabel()
        self.volume_indicator.setFixedSize(20, 40)
        self.volume_indicator.setStyleSheet("color: #FF5252; font-weight: bold;")
        self.volume_indicator.setText("🔊")
        self.volume_indicator.setVisible(False)
        self.input_layout.addWidget(self.volume_indicator)
        
        # Send button with icon
        self.send_button = QPushButton()
        self.send_button.setToolTip("Send message")
        self.send_button.setFixedSize(40, 40)
        send_icon_path = os.path.join("resources", "send_icon.svg")
        if os.path.exists(send_icon_path):
            self.send_button.setIcon(QIcon(send_icon_path))
        else:
            self.send_button.setText("Send")
        self.send_button.setStyleSheet(
            "QPushButton { background-color: #2979FF; color: white; border-radius: 20px; }"
            "QPushButton:hover { background-color: #2196F3; }"
        )
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        
        # Add the input layout to the container
        input_layout_container.addLayout(self.input_layout)
        
        # Add the input container to the main layout
        self.layout.addWidget(input_container)
        
        # Connect signals to handle messages
        self.send_message_signal.connect(self.receive_ai_response)
        
        # Add welcome message
        self.add_ai_message("Welcome! I'm your AI assistant. How can I help you today?", "Assistant Agent")
        
    def send_message(self):
        """Send a user message"""
        message = self.message_input.text().strip()
        if not message:
            return
            
        # Add user message to chat
        self.add_user_message(message)
        
        # Clear input field
        self.message_input.clear()
        
        # Get the current agent type based on button state
        is_coder = self.coder_button.isChecked()
        agent_type = "Coder Agent" if is_coder else "Assistant Agent"
        
        # Emit signal for async processing (if implemented)
        self.send_message_signal.emit(message, agent_type)
        
        if is_coder:
            # Initialize shared memory for coder agent flow
            shared = {
                "user_query": message,
                "working_dir": "./project",
                "history": [],
                "response": None
            }
            
            # Create and run the coder agent flow
            flow = create_main_flow()
            flow.run(shared)
            response = shared.get("response", "No response generated")
        else:
            # Get response from the assistant agent
            response = self.assistant_agent.get_response(message)
        
        # Add AI response to chat
        self.add_ai_message(response, agent_type)
        
    def ask_coder(self):
        """Switch to Coder Agent and prompt for message"""
        self.coder_button.setChecked(True)
        self.assistant_button.setChecked(False)
        self.message_input.setFocus()
        self.message_input.setPlaceholderText("Ask the Coder Agent about code...")
        
    def ask_assistant(self):
        """Switch to Assistant Agent and prompt for message"""
        self.assistant_button.setChecked(True)
        self.coder_button.setChecked(False)
        self.message_input.setFocus()
        self.message_input.setPlaceholderText("Ask the Assistant Agent...")
        
    def add_user_message(self, text):
        """Add a user message to the chat"""
        message_widget = ChatMessage(text, is_user=True)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
        
    def add_ai_message(self, text, agent_type=None):
        """Add an AI message to the chat"""
        message_widget = ChatMessage(text, is_user=False, agent_type=agent_type)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
        
    def receive_ai_response(self, message, agent_type):
        """Handle AI response (for asynchronous processing)"""
        # This method can be used for asynchronous responses if needed
        # Currently, the synchronous implementation in send_message() is used
        pass
        
    def scroll_to_bottom(self):
        """Scroll chat to the bottom to show latest messages"""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        
    def clear_chat(self):
        """Clear all messages from the chat"""
        # Remove all widgets from the chat layout
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                
        # Clear the assistant agent context
        self.assistant_agent.clear_context()
        
        # Add a new welcome message
        self.add_ai_message("Chat cleared. How can I help you today?", "Assistant Agent")
        
    def toggle_audio_visual_mode(self):
        """Toggle audio/visual interaction mode"""
        if self.mic_button.isChecked():
            # Update microphone button appearance
            self.mic_button.setToolTip("Stop audio/visual interaction")
            self.mic_button.setText("🔴")
            
            # Show volume indicator
            self.volume_indicator.setVisible(True)
            
            # Start audio/visual mode with screen capture directly
            self.add_ai_message("Starting audio/visual interaction mode with screen capture. I can now see and hear you. My responses will be spoken aloud.", "Assistant Agent")
            
            # Disable text input while in audio/visual mode
            self.message_input.setEnabled(False)
            self.send_button.setEnabled(False)
            
            # Start the audio/visual mode with screen capture mode
            self.audio_visual_task = self.assistant_agent.start_audio_visual_mode(video_mode="screen")
        else:
            # Update microphone button appearance
            self.mic_button.setToolTip("Start audio/visual interaction")
            self.mic_button.setText("🎤")
            
            # Hide volume indicator
            self.volume_indicator.setVisible(False)
            
            # Stop audio/visual mode
            self.add_ai_message("Audio/visual interaction mode stopped.", "Assistant Agent")
            # Re-enable text input
            self.message_input.setEnabled(True)
            self.send_button.setEnabled(True)
            # Stop the audio/visual mode
            self.assistant_agent.stop_audio_visual_mode()