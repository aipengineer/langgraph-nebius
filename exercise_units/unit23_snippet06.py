# Step 6: Error Handling
"""
Step 6: Error Processing

Key Concepts:
- Error collection
- Error message formatting
- State updates with errors
"""
# Import the HumanMessage type from langchain_core.messages
from langchain_core.messages import HumanMessage

# Reference to previously defined components
# Assuming the State class is defined in a separate file called snippets.py
from snippets import (  # Import the State class from snippets.py
    State,
)


# Define a function to handle errors from parallel execution
def error_handler(state: State) -> State:
    """Handle errors from parallel execution.

    Args:
        state: Current state with errors
    Returns:
        Updated state with error messages
    """
    messages = list(state["messages"])  # Create a copy of the messages list

    # Process errors
    for tool_id, error in state["errors"].items():  # Iterate over the errors dictionary
        # Append a HumanMessage with the tool ID and the error message to the messages list
        messages.append(
            HumanMessage(content=f"Error from {tool_id}: {error}")
        )

    # Return the updated state with the error messages
    return {
        "messages": messages,  # Update the messages list
        "pending_tools": [],  # Clear the pending_tools list
        "results": state["results"],  # Keep the results dictionary
        "errors": state["errors"]  # Keep the errors dictionary
    }


# Define a function to route to the appropriate handler based on the presence of errors
def route_results(state: State) -> str:
    """Route to appropriate handler based on errors."""
    if state.get("errors", {}):  # If there are any errors in the state
        return "error_handler"  # Route to the error_handler node
    return "result_aggregator"  # Otherwise, route to the result_aggregator node


# Example usage of the error_handler and route_results functions
state = {
    "messages": [],
    "pending_tools": [],
    "results": {},
    "errors": {"tool1": "Connection failed"}  # Example errors dictionary
}
result = error_handler(state)  # Handle the errors