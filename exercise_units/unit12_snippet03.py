# Step 3: Message Window Management
"""
Step 3: Managing Message History

Key Concepts:
- Sliding window keeps recent context
- Window size controls memory usage
- State updates maintain conversation flow
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
# Import StateGraph and START from langgraph.graph
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

# Define the State class as before
class State(TypedDict):
    """State with windowed message history."""
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int

# Define a node function called message_windowing that takes in the current state
# and returns an updated state.
def message_windowing(state: State) -> State:
    """Maintain only recent messages in state."""
    # If the number of messages exceeds the window size, truncate the messages list
    # to keep only the last window_size messages.
    if len(state["messages"]) > state["window_size"]:
        state["messages"] = state["messages"][-state["window_size"]:]
    return state

# Create basic graph with windowing
# Create a new StateGraph object
graph = StateGraph(State)
# Add the message_windowing function to the graph as a node named "windowing"
graph.add_node("windowing", message_windowing)
# Add an edge from START to "windowing" to specify the starting node in the graph
graph.add_edge(START, "windowing")

# Example usage:
# Create a state with 5 messages and a window size of 3
state = {
    "messages": [HumanMessage(content=f"Message {i}") for i in range(5)],
    "summary": "",
    "window_size": 3
}
# Call the message_windowing function with the state and print the number of messages in the result
result = message_windowing(state)
print(len(result["messages"]))  # Output: 3