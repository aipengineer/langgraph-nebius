# Step 9: Graph Construction
"""
Step 9: Building the Agent Graph

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
    State,             # From Step 1: State structure
    tool_selector,     # From Step 4: Tool selection
    execute_with_tool_node,  # From Step 6: ToolNode execution
    result_processor,  # From Step 7: Result processing
    get_next_step      # From Step 8: Flow control
)

# Define a function called create_agent_graph that creates and returns the complete agent graph
def create_agent_graph() -> StateGraph:
    """Create the complete agent graph."""
    # Create a new StateGraph object with the State defined in Step 1
    graph = StateGraph(State)

    # Add nodes to the graph
    graph.add_node("tool_selector", tool_selector)  # Add the tool_selector function as a node
    graph.add_node("tool_executor", execute_with_tool_node)  # Add the execute_with_tool_node function as a node
    graph.add_node("result_processor", result_processor)  # Add the result_processor function as a node

    # Add edges to connect the nodes in the graph
    graph.add_edge(START, "tool_selector")  # Connect the START node to the tool_selector node
    graph.add_edge("tool_selector", "tool_executor")  # Connect the tool_selector node to the tool_executor node
    graph.add_edge("tool_executor", "result_processor")  # Connect the tool_executor node to the result_processor node

    # Add conditional edges based on the get_next_step function
    graph.add_conditional_edges(
        "result_processor",  # Add conditional edges from the result_processor node
        get_next_step,  # Use the get_next_step function to determine the next step
        {
            "tool_selector": "tool_selector",  # If get_next_step returns "tool_selector", go to the tool_selector node
            "end": END  # If get_next_step returns "end", go to the END node
        }
    )

    # Return the created graph
    return graph

# Example usage:
# Call the create_agent_graph function to create the graph and compile it
graph = create_agent_graph()
chain = graph.compile()