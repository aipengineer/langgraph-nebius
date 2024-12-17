# Step 5: Multi-Node Pipeline
"""
Step 5: Complete Message Management Pipeline

Key Concepts:
- Multiple nodes form processing pipeline
- Each node handles specific functionality
- State flows through entire pipeline
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Define the State class as before
class State(TypedDict):
    """Complete state for message management."""
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str
    window_size: int

# Define the process_message node function as before
def process_message(state: State) -> State:
    """Handle message responses."""
    if not state["messages"]:
        return {
            "messages": [HumanMessage(content="Hello!")],
            "summary": "",
            "window_size": 3
        }
    return state

# Define the message_windowing node function as before
def message_windowing(state: State) -> State:
    """Maintain message window."""
    if len(state["messages"]) > state["window_size"]:
        state["messages"] = state["messages"][-state["window_size"]:]
    return state

# Define the summary_generation node function as before
def summary_generation(state: State) -> State:
    """Update conversation summary."""
    if len(state["messages"]) > 2:
        messages_text = " -> ".join([m.content for m in state["messages"]])
        state["summary"] = f"Conversation summary: {messages_text}"
    return state

# Create multi-node pipeline
# Create a new StateGraph object
graph = StateGraph(State)
# Add the three node functions to the graph
graph.add_node("processor", process_message)
graph.add_node("windowing", message_windowing)
graph.add_node("summarizer", summary_generation)

# Connect nodes in pipeline to define the flow of execution
graph.add_edge(START, "processor")
graph.add_edge("processor", "windowing")
graph.add_edge("windowing", "summarizer")
graph.add_edge("summarizer", END)

# Compile the graph to make it ready for execution
chain = graph.compile()

# Example usage:
# Create an initial state and call the compiled graph with it
state = {"messages": [], "summary": "", "window_size": 3}
result = chain.invoke(state)
# Print the content of the first message in the result
print(result["messages"][0].content)  # Output: "Hello!"