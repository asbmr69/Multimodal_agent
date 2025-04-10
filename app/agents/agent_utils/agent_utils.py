from agents.coder import CoderAgent
from agents.assistant import AssistantAgent

class AgentManager:
    """Manager class for handling different AI agents"""
    
    def __init__(self):
        # Initialize the available agents
        self.coder_agent = CoderAgent()
        self.assistant_agent = AssistantAgent()
        
        # Register agents with their display names
        self.agents = {
            "Coder Agent": self.coder_agent,
            "Assistant Agent": self.assistant_agent
        }
        
        # Conversation context
        self.context = {
            "conversation_history": []
        }
    
    def get_response(self, message, agent_type):
        """Get a response from the specified agent type"""
        # Update conversation history
        self.context["conversation_history"].append({
            "role": "user",
            "content": message
        })
        
        # Get the agent instance
        agent = self.agents.get(agent_type)
        if not agent:
            response = f"Unknown agent type: {agent_type}"
        else:
            # Process the message with the agent
            response = agent.process(message, self.context)
        
        # Add the response to conversation history
        self.context["conversation_history"].append({
            "role": "agent",
            "content": response,
            "agent_type": agent_type
        })
        
        return response
    
    def get_available_agents(self):
        """Get a list of available agent names"""
        return list(self.agents.keys())
    
    def register_agent(self, name, agent_instance):
        """Register a new agent"""
        self.agents[name] = agent_instance
        
    def clear_context(self):
        """Clear the conversation context"""
        self.context = {
            "conversation_history": []
        }


# Placeholder for actual LLM integration
def setup_llm_integration():
    """Setup for LLM integration - replace with actual setup code"""
    # In a real implementation, this would:
    # - Load API keys from environment or config
    # - Initialize LLM clients/SDKs
    # - Setup any required caching or rate limiting
    pass 