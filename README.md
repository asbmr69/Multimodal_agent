# Multimodal AI Agent Application

A desktop application built with PyQt6 that integrates AI agents for coding assistance and general queries.

## Features

- **Code Editor**: Edit and create files with syntax highlighting
- **File Explorer**: Browse, create, and manage files and folders
- **Chat Interface**: Interact with AI agents through a chat interface
- **Dual Agent System**: Switch between Coder Agent and Assistant Agent based on your needs

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

```
python app/main.py
```

## Usage

- **File Management**: Use the file explorer on the left to browse, create, and manage files
- **Code Editing**: Edit code in the central editor with syntax highlighting
- **AI Assistance**: Use the chat section on the right to interact with AI agents:
  - Select the agent type from the dropdown (Coder or Assistant)
  - Type your query and press Enter or click Send
  - Click "Ask Assistant" to quickly switch to the Assistant agent

## Project Structure

```
app/
├── components/           # UI components
│   ├── chat_section.py   # Chat interface
│   ├── code_editor.py    # Code editing component
│   ├── file_explorer.py  # File system explorer
│   └── main_window.py    # Main application window
├── utils/                # Utility modules
│   └── agent_utils.py    # AI agent implementation
└── main.py               # Application entry point
```

## Customization

To integrate with actual LLM systems, modify the `AgentManager` class in `app/utils/agent_utils.py` to connect with your preferred AI service. 