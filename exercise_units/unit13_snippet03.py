# Step 3: Response Nodes
"""
Step 3: Multiple Response Nodes

Key Concepts:
- Different nodes for different responses
- AIMessage vs HumanMessage
- Maintaining classification context
"""
from typing import Annotated, TypedDict
# Import the AIMessage type from langchain_core.messages
from langchain_core.messages import BaseMessage, AIMessage
# Import StateGraph and START from langgraph.graph
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

# Define the State class as before
class State(TypedDict):
    """State for classification and response."""
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float

# Define a node function called greeting_node that takes in the current state
# and returns an updated state.
def greeting_node(state: State) -> State:
    """Handle greeting responses."""
    # Return a new state with an AIMessage greeting, keeping the classification and confidence the same
    return {
        "messages": [AIMessage(content="Hello there!")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }

# Define another node function called help_node that takes in the current state
# and returns an updated state.
def help_node(state: State) -> State:
    """Handle help requests."""
    # Return a new state with an AIMessage offering help, keeping the classification and confidence the same
    return {
        "messages": [AIMessage(content="How can I help you?")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }

# Create basic graph with response nodes
# Create a new StateGraph object
graph = StateGraph(State)
# Add the greeting_node and help_node functions to the graph as nodes
graph.add_node("greeting", greeting_node)
graph.add_node("help", help_node)

# Example usage:
# Initialize the state with a classification of "greeting" and call the greeting_node function
state = {
    "messages": [],
    "classification": "greeting",
    "confidence": 0.9
}
result = greeting_node(state)
print(result["messages"][0].content)  # Output: "Hello there!"