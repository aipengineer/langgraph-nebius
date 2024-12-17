# Step 4: Routing Logic
"""
Step 4: Conditional Routing

Key Concepts:
- Route messages based on classification
- Use confidence scores for routing decisions
- Handle multiple possible paths
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """State for routing decisions."""
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


# Define a function called get_next_node that takes in the current state
# and returns the name of the next node to execute.
def get_next_node(state: State) -> str:
    """Determine next node based on classification and confidence."""
    # Get the classification and confidence from the state
    classification = state["classification"]
    confidence = state["confidence"]

    # Route based on confidence and classification
    if confidence > 0.8:  # High confidence routing
        if classification == "greeting":
            return "response_1"  # Route to response_1 if the classification is greeting
        elif classification == "help":
            return "response_2"  # Route to response_2 if the classification is help

    # Low confidence fallback
    return "response_3"  # Route to response_3 if the confidence is low or classification is unknown


# Create routing graph
# Create a new StateGraph object
graph = StateGraph(State)
# Add conditional edges from "classifier" to other nodes based on the get_next_node function
graph.add_conditional_edges(
    "classifier",
    get_next_node,
    {
        "response_1": "response_1",
        "response_2": "response_2",
        "response_3": "response_3"
    }
)

# Example routing based on state
# Initialize the state with a classification of "greeting" and call the get_next_node function
state = {
    "messages": [],
    "classification": "greeting",
    "confidence": 0.9
}
next_node = get_next_node(state)
print(next_node)  # Output: "response_1"