# Step 3: Rate Limiting
"""
Step 3: Implementing Rate Limits

Key Concepts:
- Usage tracking
- Rate limit checking
- Usage updates
"""
from typing import Annotated, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import AIMessage, BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages

# Define the State class with fields for rate limiting
class State(TypedDict):
    """State with rate limiting."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_usage: dict[str, int]  # A dictionary to track tool usage
    rate_limits: dict[str, int]  # A dictionary to store tool rate limits

# Define a function called check_rate_limit that takes in the current state and a tool name
# and returns a boolean indicating whether the tool has exceeded its rate limit
def check_rate_limit(state: State, tool_name: str) -> bool:
    """Check if tool has exceeded its rate limit."""
    # Get the current usage count for the tool, defaulting to 0 if not found
    usage = state["tool_usage"].get(tool_name, 0)
    # Get the rate limit for the tool, defaulting to infinity if not found
    limit = state["rate_limits"].get(tool_name, float("inf"))
    # Return True if the usage is less than the limit, False otherwise
    return usage < limit

# Define a function called update_usage that takes in the current state and a tool name
# and returns an updated state with the tool usage count incremented
def update_usage(state: State, tool_name: str) -> State:
    """Update tool usage counts."""
    # If the tool has not exceeded its rate limit
    if check_rate_limit(state, tool_name):
        # Return an updated state with the tool usage count incremented
        return {
            **state,  # Keep the existing state
            "tool_usage": {  # Update the tool_usage dictionary
                **state["tool_usage"],  # Keep the existing tool usage counts
                tool_name: state["tool_usage"].get(tool_name, 0) + 1  # Increment the count for the given tool
            }
        }
    # Otherwise, return a new state with a rate limit exceeded message
    return {
        **state,  # Keep the existing state
        "messages": [AIMessage(content=f"Rate limit exceeded for {tool_name}")]  # Add a rate limit exceeded message
    }

# Example usage:
# Initialize the state with tool usage and rate limits and call the check_rate_limit function
state = {
    "messages": [],
    "tool_usage": {"calculator": 2},  # Set the current usage count for the calculator tool
    "rate_limits": {"calculator": 3}  # Set the rate limit for the calculator tool
}
result = check_rate_limit(state, "calculator")
print(result)  # Output: True