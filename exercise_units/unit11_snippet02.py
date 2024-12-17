# Step 2: Messages and BaseMessage
"""
Step 2: Working with LangChain Messages

Key Concepts:
- BaseMessage is the foundation for all message types
- HumanMessage represents user input
- Messages have content and type
"""
from typing import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage


# Update our state to use a more specific type for messages
class State(TypedDict):
    """State for our conversational graph.

    Now we specify that our messages must be BaseMessage objects,
    which provides structure and type safety.
    """
    # The `messages` key will be a list of BaseMessage objects.
    # This means we can't add anything to this list apart from these objects.
    messages: list[BaseMessage]


# Example usage:
state: State = {"messages": []}
# Create a new HumanMessage object with the content "Hello!"
hello_message = HumanMessage(content="Hello!")
# Append the message to the list
state["messages"].append(hello_message)
# Print the content of the first message in the list
print(state["messages"][0].content)  # Output: "Hello!"

