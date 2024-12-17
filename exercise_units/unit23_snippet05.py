# Step 5: Result Aggregation
"""
Step 5: Fan-in Pattern

Key Concepts:
- Result aggregation
- Binary operator aggregation
- Dictionary reduction
"""
from typing import Dict, TypedDict, Annotated, Any  # Import necessary types for type hinting
# Import the BinaryOperatorAggregate class from langgraph.channels.binop
from langgraph.channels.binop import BinaryOperatorAggregate
# Import necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages
import json  # Import the json library for encoding tool results


# Define a reducer function to combine two dictionaries
def dict_reducer(a: dict, b: dict | None) -> dict:
    """Combine two dictionaries for aggregation."""
    if b is None:  # If the second dictionary is None, return the first dictionary
        return a
    return {**a, **b}  # Otherwise, merge the two dictionaries and return the result


# Define the State class with aggregation support for the results and errors dictionaries
class State(TypedDict):
    """State with aggregation support."""
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]
    # The results and errors keys are annotated with the BinaryOperatorAggregate class.
    # This tells LangGraph that whenever it receives an update to these keys
    # that it should use this class to apply the update.
    # We'll see how this is used in the result_aggregator and error_handler functions below.
    results: Annotated[dict[str, Any], BinaryOperatorAggregate(Dict[str, Any], dict_reducer)]
    errors: Annotated[dict[str, str], BinaryOperatorAggregate(Dict[str, str], dict_reducer)]


# Define a function to aggregate results from parallel execution
def result_aggregator(state: State) -> State:
    """Aggregate results from parallel execution."""
    messages = list(state["messages"])  # Create a copy of the messages list

    # Process successful results
    for tool_id, result in state["results"].items():  # Iterate over the results dictionary
        # Append a HumanMessage with the tool ID and the result to the messages list
        messages.append(
            HumanMessage(content=f"Result from {tool_id}: {json.dumps(result)}")  # Encode the result as a JSON string
        )

    # Return the updated state with the aggregated results
    return {
        "messages": messages,  # Update the messages list
        "pending_tools": [],  # Clear the pending_tools list
        "results": state["results"],  # Keep the results dictionary
        "errors": state["errors"]  # Keep the errors dictionary
    }


# Example usage of the result_aggregator function
state = {
    "messages": [],
    "pending_tools": [],
    "results": {"tool1": "result1", "tool2": "result2"},  # Example results dictionary
    "errors": {}
}
result = result_aggregator(state)  # Aggregate the results