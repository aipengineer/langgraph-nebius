# Step 1: Enhanced State Structure
"""
Step 1: State for Multi-Tool Agents

Key Concepts:
- TypedDict with optional fields
- Tool tracking in state
- Rate limit configuration
"""
from typing import Annotated, Any, NotRequired, TypedDict
# Import the necessary message type from langchain_core.messages
from langchain_core.messages import BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class with additional fields to manage multi-tool operations
class State(TypedDict, total=False):
    """Enhanced state for multi-tool operations.

    Fields:
    - messages: Conversation history
    - available_tools: List of tools agent can use
    - tool_usage: Tracks how many times each tool is used
    - rate_limits: Maximum uses for each tool
    - tool_name: Currently selected tool
    - tool_outputs: Results from tool executions
    """
    # Annotated[list[BaseMessage], add_messages] indicates that the messages field
    # should be treated as a list of BaseMessage objects and that the add_messages
    # function should be used to handle updates to this field.
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]  # A list to store the available tools
    tool_usage: dict[str, int]  # A dictionary to track tool usage
    rate_limits: dict[str, int]  # A dictionary to store tool rate limits
    tool_name: NotRequired[str | None]  # An optional field to store the currently selected tool name
    tool_outputs: NotRequired[list[str]]  # An optional field to store tool execution results


# Example usage:
# Initialize the state with a list of messages, available tools, tool usage, and rate limits
state: State = {
    "messages": [],
    "available_tools": [],
    "tool_usage": {"calculator": 0, "weather": 0},  # Initialize tool usage counts
    "rate_limits": {"calculator": 3, "weather": 1},  # Set rate limits for each tool
}
print(state)