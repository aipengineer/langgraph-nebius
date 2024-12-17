# Step 1: Extended State
"""
Step 1: Extended State Management

Key Concepts:
- State can hold multiple fields beyond messages
- Additional fields help manage conversation context
- TypedDict allows flexible state structure
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


# Define the State class with additional fields to manage conversation context
class State(TypedDict):
    """Enhanced state that manages conversation context.

    Fields:
    - messages: List of conversation messages
    - summary: Current conversation summary
    - window_size: Number of messages to keep in memory
    """
    # Annotated[list[BaseMessage], add_messages] indicates that the messages field
    # should be treated as a list of BaseMessage objects and that the add_messages
    # function should be used to handle updates to this field.
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str  # A string to store the conversation summary
    window_size: int  # An integer to control the number of messages to keep


# Example usage:
# Initialize the state with an empty list of messages, an empty summary, and a window size of 3
state: State = {
    "messages": [],
    "summary": "",
    "window_size": 3
}
print(state)  # Output: {'messages': [], 'summary': '', 'window_size': 3}

