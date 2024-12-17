# Step 2: Message Processing Node
"""
Step 2: Enhanced Message Processing

Key Concepts:
- Nodes can access and modify multiple state fields
- State updates maintain all fields
- Response generation with context awareness
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """State with conversation context."""
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int


# Define a node function called process_message that takes in the current state
# and returns an updated state.
def process_message(state: State) -> State:
    """Process messages with context awareness."""
    # If there are no messages in the state, return a new state with a "Hello!" message,
    # an empty summary, and a window size of 3.
    if not state["messages"]:
        return {
            "messages": [HumanMessage(content="Hello!")],
            "summary": "",
            "window_size": 3
        }

    # Otherwise, get the last message and check its content
    last_message = state["messages"][-1]
    if last_message.content == "Hello!":
        # If the content is "Hello!", return a new state with a "How are you?" message,
        # keeping the summary and window size the same.
        return {
            "messages": [HumanMessage(content="How are you?")],
            "summary": state["summary"],
            "window_size": state["window_size"]
        }

    # Otherwise, return the state unchanged.
    return state


# Example usage:
# Call the process_message function with an initial state and print the content of the first message
state = process_message({"messages": [], "summary": "", "window_size": 3})
print(state["messages"][0].content)  # Output: "Hello!"