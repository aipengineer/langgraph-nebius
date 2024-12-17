# Step 1: Tool State Setup
"""
Step 1: Setting up Tool-Enabled State

Key Concepts:
- State structure for tool usage
- Configuration management
- Tool initialization
"""
import os
from typing import Annotated, Any, TypedDict
# Import the necessary message type from langchain_core.messages
from langchain_core.messages import BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults
# Import the BaseSettings and SettingsConfigDict classes from pydantic_settings
from pydantic_settings import BaseSettings, SettingsConfigDict


# Define the Settings class to manage configuration for our tool-enabled agent
class Settings(BaseSettings):
    """Configuration for our tool-enabled agent."""
    tavily_api_key: str  # Define an attribute to store the Tavily API key

    # Configure the settings to load from a .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


# Define the State class with additional fields to manage tool usage and results
class State(TypedDict):
    """State that tracks tool usage and results.

    Fields:
    - messages: Conversation history
    - tool_calls: Record of tools being called
    - tool_outputs: Results from tool executions
    """
    # Annotated[list[BaseMessage], add_messages] indicates that the messages field
    # should be treated as a list of BaseMessage objects and that the add_messages
    # function should be used to handle updates to this field.
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]  # A list to store tool call information
    tool_outputs: list[Any]  # A list to store tool execution results


# Initialize settings and tool
# Create an instance of the Settings class to load the configuration
settings = Settings()
# Set the Tavily API key in the environment variable
os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
# Create an instance of the TavilySearchResults tool
tavily_tool = TavilySearchResults()

# Example usage:
# Initialize the state with empty lists for messages, tool_calls, and tool_outputs
state: State = {
    "messages": [],
    "tool_calls": [],
    "tool_outputs": []
}
print(state)  # Output: {'messages': [], 'tool_calls': [], 'tool_outputs': []}