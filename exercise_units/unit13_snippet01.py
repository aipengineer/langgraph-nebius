# Step 1: Classification State
"""
Step 1: State with Classification

Key Concepts:
- State can track message classification
- Classification includes confidence scores
- Different message types (Human vs AI)
"""
from typing import Annotated, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.graph.message import add_messages


# Define the State class with additional fields to manage message classification
class State(TypedDict):
    """State that includes classification information.

    Fields:
    - messages: List of conversation messages
    - classification: Category of the message
    - confidence: Confidence score of classification
    """
    # Annotated[list[BaseMessage], add_messages] indicates that the messages field
    # should be treated as a list of BaseMessage objects and that the add_messages
    # function should be used to handle updates to this field.
    messages: Annotated[list[BaseMessage], add_messages]
    classification: str  # A string to store the classification of the message
    confidence: float  # A float to store the confidence score of the classification


# Example usage:
# Initialize the state with a HumanMessage, a classification of "greeting", and a confidence of 0.9
state: State = {
    "messages": [HumanMessage(content="hello there")],
    "classification": "greeting",
    "confidence": 0.9
}
print(
    state)  # Output: {'messages': [HumanMessage(content='hello there')], 'classification': 'greeting', 'confidence': 0.9}