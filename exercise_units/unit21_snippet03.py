# Step 3: Tool Execution
"""
Step 3: Executing Tools

Key Concepts:
- Tool execution flow
- Error handling
- JSON response handling
"""
import json
from typing import Annotated, Any, TypedDict
# Import the necessary message type from langchain_core.messages
from langchain_core.messages import BaseMessage
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """State for tool execution."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


# Define a node function called tool_executor that takes in the current state
# and returns an updated state.
def tool_executor(state: State) -> State:
    """Execute tools and handle results."""
    # If there are no tool calls in the state, return an empty list of tool outputs
    if not state.get("tool_calls"):
        return {"tool_outputs": []}

    # Get the last tool call from the tool_calls list
    tool_call = state["tool_calls"][-1]
    # Create an instance of the TavilySearchResults tool
    tavily_tool = TavilySearchResults()

    try:
        # If the tool name is "TavilySearchResults", execute the tool with the given arguments
        if tool_call["tool_name"] == "TavilySearchResults":
            output = tavily_tool.invoke(tool_call["args"])
            # Return the tool output as a JSON string in the tool_outputs list
            return {"tool_outputs": [json.dumps(output)]}
    except Exception as e:
        # If there is an error during tool execution, return the error message as a JSON string
        return {"tool_outputs": [json.dumps({"error": str(e)})]}

    # Otherwise, return an empty list of tool outputs
    return {"tool_outputs": []}


# Example usage:
# Initialize the state with a tool call to TavilySearchResults and call the tool_executor function
state = {
    "tool_calls": [{
        "tool_name": "TavilySearchResults",
        "args": {"query": "capital of France"}
    }],
    "messages": [],
    "tool_outputs": []
}
result = tool_executor(state)
# Print whether a tool output was received
print("Tool output received:", bool(result["tool_outputs"]))