# Step 2: Tool Configuration
"""
Step 2: Setting Up Tools

Key Concepts:
- Tool initialization
- Mock tool for testing
- Tool call structure
"""
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults
# Import the HumanMessage type from langchain_core.messages
from langchain_core.messages import HumanMessage

# Define a mock tool function for testing parallel execution
def mock_tool(query: str = "mock query") -> dict:
    """Mock tool for testing parallel execution."""
    # Create a HumanMessage with the query
    message = HumanMessage(content=f"Mock tool called with query: {query}")
    # Return a dictionary with the message, results, and an empty errors dictionary
    return {
        "messages": [message],
        "results": {"mock_tool": "mock_value"},  # Mock result value
        "errors": {}
    }

# Initialize the real TavilySearchResults tool
tavily_tool = TavilySearchResults()

# Example tool calls for both the real and mock tools
real_tool_call = {
    "id": "search_1",
    "tool_name": "TavilySearchResults",
    "args": {"query": "capital of France"}
}

mock_tool_call = {
    "id": "mock_1",
    "tool_name": "mock_tool",
    "args": {"query": "test query"}
}

# Test the mock tool function and print the results
result = mock_tool("test query")
print(result["results"])  # Output: {"mock_tool": "mock_value"}