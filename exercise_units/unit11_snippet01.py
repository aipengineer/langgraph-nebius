# Step 1: Understanding State
"""
Step 1: Understanding State in LangGraph

Key Concepts:
- State is a container for your conversation's data
- TypedDict provides type safety for dictionaries
- State will store our messages
"""
from typing import TypedDict


# Define the structure of our state using TypedDict
# This is similar to a dictionary, but provides type safety,
# meaning we get errors if we try to add keys with the wrong data type.
class State(TypedDict):
    """State for our conversational graph.

    In LangGraph, state holds all the data that flows through our graph.
    For now, we'll just define a simple messages field.
    """
    # The `messages` key will be a list.
    # We'll make this more specific later
    messages: list


# Example usage:
# Create a new state with an empty list of messages
state: State = {"messages": []}
# Append a message to the list
state["messages"].append("Hello!")
# Print the updated state
print(state)  # Output: {'messages': ['Hello!']}

