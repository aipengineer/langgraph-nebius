# Step 2: Basic Classification Node
"""
Step 2: Message Classification

Key Concepts:
- Nodes can classify messages
- Classification preserves existing messages
- Confidence scores indicate certainty
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages

# Define the State class as before
class State(TypedDict):
    """State for message classification."""
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str
    confidence: float

# Define a node function called classifier_node that takes in the current state
# and returns an updated state.
def classifier_node(state: State) -> State:
    """Classify the last message in the conversation."""
    # Get the content of the last message in the messages list
    message = state["messages"][-1].content

    # Classify the message based on its content
    if "hello" in message.lower():
        # If the message contains "hello", classify it as a greeting with high confidence
        return {
            "messages": state["messages"],  # Keep the existing messages
            "classification": "greeting",
            "confidence": 0.9
        }
    else:
        # Otherwise, classify it as unknown with low confidence
        return {
            "messages": state["messages"],  # Keep the existing messages
            "classification": "unknown",
            "confidence": 0.1
        }

# Example usage:
# Initialize the state with a HumanMessage and call the classifier_node function
state = {
    "messages": [HumanMessage(content="Hello!")],
    "classification": "",
    "confidence": 0.0
}
result = classifier_node(state)
print(result["classification"])  # Output: "greeting"
print(result["confidence"])      # Output: 0.9