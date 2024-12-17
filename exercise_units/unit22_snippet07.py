# Step 7: Result Processing
"""
Step 7: Processing Tool Results

Key Concepts:
- Output formatting
- Message generation
- State updates
"""
from typing import Annotated, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import AIMessage, BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class with fields for result processing
class State(TypedDict):
    """State for result processing."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_outputs: list[str]  # A list to store tool execution results


# Define a node function called result_processor that takes in the current state
# and returns an updated state with the formatted tool output as a message
def result_processor(state: State) -> State:
    """Process and format tool execution results."""
    # If there are no tool outputs in the state, return the state unchanged
    if not state.get("tool_outputs"):
        return state

    # Get the last tool output from the tool_outputs list
    tool_output = state["tool_outputs"][-1]

    # Format the output as a message
    formatted_output = str(tool_output)
    # If the output contains an error message, add a sorry message
    if "error" in formatted_output.lower():
        formatted_output = f"Sorry, there was an error: {formatted_output}"

    # Return an updated state with the formatted output as an AIMessage in the messages list
    return {
        **state,  # Keep the existing state
        "messages": state.get("messages", []) + [  # Add the formatted output to the messages list
            AIMessage(content=formatted_output)
        ]
    }


# Example usage:
# Initialize the state with a tool output and call the result_processor function
state = {
    "messages": [],
    "tool_outputs": ["Temperature is 72°F"]
}
result = result_processor(state)
# Print the content of the last message in the result
print(result["messages"][-1].content)  # Output: "Temperature is 72°F"