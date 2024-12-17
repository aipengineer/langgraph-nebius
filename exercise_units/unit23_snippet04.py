# Step 4: Parallel Execution
"""
Step 4: Running Tools in Parallel

Key Concepts:
- Concurrent execution
- Task gathering
- Result collection
"""
import asyncio  # Import the asyncio library for asynchronous operations
from typing import Annotated, Any, TypedDict  # Import necessary types for type hinting
# Import necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages

# Reference to previously defined components
# Assuming the execute_tool function is defined in a separate file called snippets.py
from snippets import (  # Normally from your implementation
    execute_tool,  # Import the execute_tool function
)


# Define the State class as before
class State(TypedDict):
    """State for parallel execution."""
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    results: dict[str, Any]
    errors: dict[str, str]


# Define an asynchronous function to execute multiple tools in parallel
async def parallel_executor(state: State) -> State:
    """Execute multiple tools in parallel.

    Args:
        state: Current state with pending tools
    Returns:
        Updated state with results
    """
    # If there are no pending tools, return the state unchanged
    if not state["pending_tools"]:
        return state

    # Create a list of tasks for each pending tool call
    tasks = [
        execute_tool(tool_call)  # Create an asynchronous task for each tool call
        for tool_call in state["pending_tools"]  # Iterate over the pending tool calls
    ]

    # Execute all tasks concurrently using asyncio.gather
    results = await asyncio.gather(*tasks)  # Execute all tasks concurrently and wait for the results

    # Process the results and separate them into successful results and errors
    new_results = {}  # Dictionary to store successful results
    new_errors = {}  # Dictionary to store errors

    for tool_id, result in results:  # Iterate over the results from each tool call
        if isinstance(result, str) and result.startswith("Error:"):  # Check if the result is an error message
            new_errors[tool_id] = result  # Store the error message in the new_errors dictionary
        else:
            new_results[tool_id] = result  # Store the successful result in the new_results dictionary

    # Return the updated state with the results and errors
    return {
        "messages": state["messages"],  # Keep the existing messages
        "pending_tools": [],  # Clear the pending_tools list
        "results": new_results,  # Update the results dictionary
        "errors": new_errors  # Update the errors dictionary
    }

# Example usage of the parallel_executor function in a graph:
# graph.add_node("parallel_executor", parallel_executor)  # Add the function as a node to the graph