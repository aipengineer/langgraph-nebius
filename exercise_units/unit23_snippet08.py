# Step 8: Graph Structure
"""
Step 8: Graph Configuration

Key Concepts:
- Node addition
- Edge configuration
- Conditional routing
"""
# Import END, START, and StateGraph from langgraph.graph
from langgraph.graph import END, START, StateGraph

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


# Define a function called create_parallel_graph that creates and returns the graph for parallel execution
def create_parallel_graph() -> StateGraph:
    """Create graph for parallel execution."""
    # Create a new StateGraph object with the State defined in Step 1
    graph = StateGraph(State)

    # Add nodes to the graph
    graph.add_node("init", get_initial_state)  # Add the get_initial_state function as a node named "init"
    graph.add_node("parallel_executor", parallel_executor)  # Add the parallel_executor function as a node
    graph.add_node("result_aggregator", result_aggregator)  # Add the result_aggregator function as a node
    graph.add_node("error_handler", error_handler)  # Add the error_handler function as a node

    # Add basic flow edges to connect the nodes in sequence
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

    # Return the created graph
    return graph


# Example usage of the create_parallel_graph function
graph = create_parallel_graph()  # Create the graph for parallel execution