from abc import ABC, abstractmethod
import os
import json

class BaseAgent(ABC):
    """Base class for all AI agents in the system"""
    
    def __init__(self, name, description=None):
        """
        Initialize the base agent
        
        Args:
            name (str): Name of the agent
            description (str, optional): Description of what the agent does
        """
        self.name = name
        self.description = description or f"{name} Agent"
        self.config = {}
        
    @abstractmethod
    def process(self, query, context=None):
        """
        Process a query and return a response
        
        Args:
            query (str): The user's query
            context (dict, optional): Additional context for the query
            
        Returns:
            str: The agent's response
        """
        pass
    
    def load_config(self, config_path=None):
        """
        Load configuration from a JSON file
        
        Args:
            config_path (str, optional): Path to the config file
        """
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                self.name.lower().replace(" ", "_") + "_config.json"
            )
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {str(e)}")
    
    def save_config(self, config_path=None):
        """
        Save the current configuration to a JSON file
        
        Args:
            config_path (str, optional): Path to save the config file
        """
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                self.name.lower().replace(" ", "_") + "_config.json"
            )
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            
    def get_metadata(self):
        """
        Get metadata about this agent
        
        Returns:
            dict: Agent metadata
        """
        return {
            "name": self.name,
            "description": self.description,
            "config": self.config
        } 