# Step 3: Graph Components
"""
Step 3: Building a Simple Graph

Key Concepts:
- StateGraph is the main graph structure
- Nodes process state
- Edges connect nodes
"""
from typing import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
# Import the StateGraph, START, and END objects from the langgraph library
from langgraph.graph import StateGraph, START, END

# Define the state as before
class State(TypedDict):
    """State for our conversational graph."""
    messages: list[BaseMessage]

# Define a node function called `simple_node`
# This function takes in the current state and returns an updated state.
# In LangGraph, nodes typically do the work.
def simple_node(state: State) -> State:
    """A simple node that adds a greeting."""
    # Return a dictionary under the key `messages` containing a list with a new HumanMessage
    return {"messages": [HumanMessage(content="Hello!")]}

# Create and compile the graph
# Create a new StateGraph
graph = StateGraph(State)
# Add the `simple_node` function to the graph under the name "greeter"
graph.add_node("greeter", simple_node)
# Add an edge from the START node to the "greeter" node.
# The START node is a special LangGraph node that represents the beginning of the graph.
# Adding an edge from START to "greeter" tells the graph that the first
# node to call is "greeter"
graph.add_edge(START, "greeter")
# Add an edge from "greeter" to the END node.
# The END node is a special LangGraph node that represents the end of the graph.
# Adding an edge from "greeter" to END tells the graph that there is nothing
# left to do after the "greeter" node completes its work.
graph.add_edge("greeter", END)
# Compile the graph. You MUST compile the graph before you can use it.
chain = graph.compile()

# Example usage:
# Call the graph on an empty state
result = chain.invoke({"messages": []})
# Print out the content of the first message in the result
print(result["messages"][0].content)  # Output: "Hello!"

