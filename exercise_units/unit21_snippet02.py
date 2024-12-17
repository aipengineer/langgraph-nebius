# Step 2: Tool Calling Node
"""
Step 2: Creating Tool Calls

Key Concepts:
- Determining when to use tools
- Structuring tool calls
- Tool call parameters
"""
import json
from typing import Annotated, Any, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """State for tool interactions."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


# Define a node function called llm_node that takes in the current state
# and returns an updated state.
def llm_node(state: State) -> State:
    """Decide when and how to call tools."""
    # Handle initial state
    # If there are no messages in the state, add a HumanMessage asking about the capital of France
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="What is the capital of France?")],
            "tool_calls": [],
            "tool_outputs": []
        }

    # Check if we need to use the tool
    # Get the content of the last message in the messages list
    last_message = state["messages"][-1].content
    # If the last message contains "capital of France", create a tool call to TavilySearchResults
    if "capital of France" in last_message:
        return {
            "tool_calls": [{  # Add a tool call to the tool_calls list
                "tool_name": "TavilySearchResults",  # Specify the name of the tool
                "args": {"query": "capital of France"}  # Specify the arguments to the tool
            }]
        }

    # Otherwise, return the state unchanged
    return state


# Example usage:
# Initialize the state with a HumanMessage and call the llm_node function
state = {
    "messages": [HumanMessage(content="What is the capital of France?")],
    "tool_calls": [],
    "tool_outputs": []
}
result = llm_node(state)
# Print the tool_calls in JSON format
print(json.dumps(result["tool_calls"], indent=2))
# Output: [{"tool_name": "TavilySearchResults", "args": {"query": "capital of France"}}]