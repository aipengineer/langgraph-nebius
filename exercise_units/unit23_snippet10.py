# Step 10: Complete Integration
"""
Step 10: Full System Integration

Key Concepts:
- Complete workflow
- State management
- Parallel execution
"""
import asyncio  # Import the asyncio library for asynchronous operations
import json  # Import the json library for encoding tool results
from typing import Annotated, Any, TypedDict, Dict  # Import necessary types for type hinting
# Import necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import END, START, and StateGraph from langgraph.graph
from langgraph.graph import END, START, StateGraph
# Import the BinaryOperatorAggregate class from langgraph.channels.binop
from langgraph.channels.binop import BinaryOperatorAggregate
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages

# Reference to previously defined components
# Assuming these components are defined in a separate file called snippets.py
from snippets import (  # Normally from your implementation
    State,  # From Step 1: State structure
    dict_reducer,  # From Step 5: Result Aggregation
    get_initial_state,  # From Step 7: State Initialization
    parallel_executor,  # From Step 4: Parallel Execution
    result_aggregator,  # From Step 5: Result Aggregation
    error_handler,  # From Step 6: Error Processing
    route_results  # From Step 6: Error Processing
)


# Define the State class with aggregation support for the results and errors dictionaries
class State(TypedDict):
    """Complete state for parallel execution system."""
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    results: Annotated[dict[str, Any], BinaryOperatorAggregate(Dict[str, Any], dict_reducer)]
    errors: Annotated[dict[str, str], BinaryOperatorAggregate(Dict[str, str], dict_reducer)]


# Define a function called create_parallel_system that creates and returns a complete parallel execution system
def create_parallel_system():
    """Create complete parallel execution system."""
    # Initialize graph
    graph = StateGraph(State)  # Create a new StateGraph object with the State defined earlier

    # Add all nodes to the graph
    graph.add_node("init", get_initial_state)  # Add the get_initial_state function as a node named "init"
    graph.add_node("parallel_executor", parallel_executor)  # Add the parallel_executor function as a node
    graph.add_node("result_aggregator", result_aggregator)  # Add the result_aggregator function as a node
    graph.add_node("error_handler", error_handler)  # Add the error_handler function as a node

    # Configure the flow of execution by adding edges
    graph.add_edge(START, "init")  # Connect the START node to the "init" node
    graph.add_edge("init", "parallel_executor")  # Connect the "init" node to the "parallel_executor" node

    # Add conditional routing edges based on the route_results function
    graph.add_conditional_edges(
        "parallel_executor",  # Add conditional edges from the "parallel_executor" node
        route_results,  # Use the route_results function to determine the next node
        {
            "result_aggregator": "result_aggregator",  # If route_results returns "result_aggregator", go to that node
            "error_handler": "error_handler"  # If route_results returns "error_handler", go to that node
        }
    )

    # Add end edges to connect the result and error handling nodes to the END node
    graph.add_edge("result_aggregator", END)  # Connect the "result_aggregator" node to the END node
    graph.add_edge("error_handler", END)  # Connect the "error_handler" node to the END node

    # Compile and return the created graph
    return graph.compile()


# Example usage of the create_parallel_system function
system = create_parallel_system()  # Create the complete parallel execution system
initial_state = get_initial_state()  # Get the initial state
result = system.invoke(initial_state)  # Invoke the system with the initial state