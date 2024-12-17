# Step 1: Parallel State Structure
"""
Step 1: State for Parallel Tool Execution

Key Concepts:
- State structure for parallel operations
- Tracking pending tools
- Result storage
"""
from typing import Annotated, Any, TypedDict
# Import necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class to manage parallel tool execution
class State(TypedDict):
    """State for parallel tool execution.

    Fields:
    - messages: Conversation history
    - pending_tools: Tools waiting to be executed
    - results: Tool execution results
    - errors: Error messages by tool ID
    """
    # Annotated[list[BaseMessage], add_messages] indicates that the messages field
    # should be treated as a list of BaseMessage objects and that the add_messages
    # function should be used to handle updates to this field.
    messages: Annotated[list[BaseMessage], add_messages]
    pending_tools: list[dict]  # A list to store pending tool calls
    results: dict[str, Any]  # A dictionary to store tool execution results
    errors: dict[str, str]  # A dictionary to store error messages


# Example usage:
# Initialize the state with a message and two pending tool calls
state = {
    "messages": [HumanMessage(content="Starting parallel execution...")],
    "pending_tools": [
        {
            "id": "search_1",  # Unique ID for the tool call
            "tool_name": "TavilySearchResults",  # Name of the tool
            "args": {"query": "capital of France"}  # Arguments to the tool
        },
        {
            "id": "search_2",  # Unique ID for the tool call
            "tool_name": "TavilySearchResults",  # Name of the tool
            "args": {"query": "largest city in Japan"}  # Arguments to the tool
        }
    ],
    "results": {},  # Empty dictionary to store results
    "errors": {}  # Empty dictionary to store errors
}
# Access the ID of the first pending tool call
print(state["pending_tools"][0]["id"])  # Output: "search_1"