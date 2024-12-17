# Step 7: State Initialization
"""
Step 7: State Setup and Initialization

Key Concepts:
- Initial state creation
- Default values
- Tool task setup
"""
# Import the HumanMessage type from langchain_core.messages
from langchain_core.messages import HumanMessage

# Reference to previously defined components
# Assuming the State class is defined in a separate file called snippets.py
from snippets import (  # Import the State class from snippets.py
    State,
)


# Define a function to get the initial state with tool configuration
def get_initial_state(use_mock: bool = False) -> State:
    """Get initial state with tool configuration."""
    # If use_mock is True, return a state with mock tool calls
    if use_mock:
        return {
            "messages": [HumanMessage(content="Starting parallel execution...")],
            "pending_tools": [
                {
                    "id": "mock_1",  # Unique ID for the mock tool call
                    "tool_name": "mock_tool",  # Name of the mock tool
                    "args": {"query": "mock query 1"}  # Arguments to the mock tool
                },
                {
                    "id": "mock_2",  # Unique ID for the mock tool call
                    "tool_name": "mock_tool",  # Name of the mock tool
                    "args": {"query": "mock query 2"}  # Arguments to the mock tool
                }
            ],
            "results": {},  # Empty dictionary to store results
            "errors": {}  # Empty dictionary to store errors
        }

    # Otherwise, return a state with real Tavily tool calls
    return {
        "messages": [HumanMessage(content="Starting parallel execution...")],
        "pending_tools": [
            {
                "id": "search_1",  # Unique ID for the Tavily tool call
                "tool_name": "TavilySearchResults",  # Name of the Tavily tool
                "args": {"query": "capital of France"}  # Arguments to the Tavily tool
            },
            {
                "id": "search_2",  # Unique ID for the Tavily tool call
                "tool_name": "TavilySearchResults",  # Name of the Tavily tool
                "args": {"query": "largest city in Japan"}  # Arguments to the Tavily tool
            }
        ],
        "results": {}, "results": {},
        "errors": {}
    }

# Example usage:
state_with_mock = get_initial_state(use_mock=True)
state_with_real = get_initial_state(use_mock=False) # Empty dictionary to store results