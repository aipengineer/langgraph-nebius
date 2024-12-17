# Step 4: Summary Generation
"""
Step 4: Conversation Summarization

Key Concepts:
- State can track conversation summary
- Summary updates based on message history
- Multiple nodes can modify different state fields
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

# Define the State class as before
class State(TypedDict):
    """State with summary management."""
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int

# Define a node function called summary_generation that takes in the current state
# and returns an updated state.
def summary_generation(state: State) -> State:
    """Generate summary from conversation history."""
    # If there are more than 2 messages, generate a summary by joining the message
    # contents with " -> " and store it in the summary field.
    if len(state["messages"]) > 2:
        messages_text = " -> ".join([m.content for m in state["messages"]])
        state["summary"] = f"Conversation summary: {messages_text}"
    return state

# Create graph with summary node
graph = StateGraph(State)
# Add the summary_generation function to the graph as a node named "summarizer"
graph.add_node("summarizer", summary_generation)
# Add an edge from START to "summarizer" to specify the starting node in the graph
graph.add_edge(START, "summarizer")

# Example usage with multiple messages
# Create a list of messages and a state with those messages
messages = [
    HumanMessage(content="Hello"),
    HumanMessage(content="How are you"),
    HumanMessage(content="Goodbye")
]
state = {"messages": messages, "summary": "", "window_size": 3}
# Call the summary_generation function with the state and print the summary
result = summary_generation(state)
print(result["summary"])  # Output: "Conversation summary: Hello -> How are you -> Goodbye"