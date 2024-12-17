# Step 5: Complete Router
"""
Step 5: Complete Classification and Routing System

Key Concepts:
- Full pipeline with classification and routing
- Multiple response paths
- Confidence-based decisions
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """Complete state for routing system."""
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float


# Define the classifier_node function as before
def classifier_node(state: State) -> State:
    """Classify incoming messages."""
    message = state["messages"][-1].content

    # Classify the message based on its content
    if "hello" in message.lower():
        return {
            "messages": state["messages"],
            "classification": "greeting",
            "confidence": 0.9
        }
    elif "help" in message.lower():
        return {
            "messages": state["messages"],
            "classification": "help",
            "confidence": 0.8
        }
    return {
        "messages": state["messages"],
        "classification": "unknown",
        "confidence": 0.1
    }


# Define the response_node_1 function as before
def response_node_1(state: State) -> State:
    """Handle greetings."""
    return {
        "messages": [AIMessage(content="Hello there!")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }


# Define the response_node_2 function as before
def response_node_2(state: State) -> State:
    """Handle help requests."""
    return {
        "messages": [AIMessage(content="How can I help you?")],
        "classification": state["classification"],
        "confidence": state["confidence"]
    }


# Define the get_next_node function as before
def get_next_node(state: State) -> str:
    """Route based on classification and confidence."""
    if state["confidence"] > 0.8:
        if state["classification"] == "greeting":
            return "response_1"
        elif state["classification"] == "help":
            return "response_2"
    return "response_3"


# Create complete routing graph
# Create a new StateGraph object
graph = StateGraph(State)

# Add nodes to the graph
graph.add_node("classifier", classifier_node)
graph.add_node("response_1", response_node_1)
graph.add_node("response_2", response_node_2)

# Connect nodes to define the flow of execution
graph.add_edge(START, "classifier")
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
# Add edges from the response nodes to the END node
graph.add_edge("response_1", END)
graph.add_edge("response_2", END)
graph.add_edge("response_3", END)

# Compile the graph to make it ready for execution
chain = graph.compile()

# Example usage:
# Initialize the state and call the compiled graph with it
state = {
    "messages": [],
    "classification": "",
    "confidence": 0.0
}
result = chain.invoke(state)