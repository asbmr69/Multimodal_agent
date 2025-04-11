import os
from typing import Tuple

def create_file(target_file: str, content: str = "") -> Tuple[str, bool]:
    """
    Create a new file or directory.
    
    Args:
        target_file: Path to the file/directory to create
        content: Content to write to the file (empty string for directories)
    
    Returns:
        Tuple of (result message, success status)
    """
    try:
        # Get absolute path
        abs_path = os.path.abspath(target_file)
        
        # Check if it's meant to be a directory (ends with / or \)
        is_dir = target_file.endswith(('/','\\'))
        
        if is_dir:
            # Create directory and parents if they don't exist
            os.makedirs(abs_path, exist_ok=True)
            return f"Successfully created directory: {target_file}", True
        else:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            
            # Check if file already exists
            if os.path.exists(abs_path):
                return f"File already exists: {target_file}", False
            
            # Create the file with content
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully created file: {target_file}", True
            
    except Exception as e:
        return f"Error creating file/directory: {str(e)}", False