# Step 3: Async Tool Execution
"""
Step 3: Asynchronous Tool Execution

Key Concepts:
- Async/await pattern
- Single tool execution
- Error handling
"""
import asyncio  # Import the asyncio library for asynchronous operations
from typing import Any  # Import Any for type hinting
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults

# Reference to previously defined components
# Assuming the mock_tool function is defined in a separate file called snippets.py
from snippets import (  # Normally from your implementation
    mock_tool,  # Import the mock_tool function
)

# Initialize the real TavilySearchResults tool
tavily_tool = TavilySearchResults()


# Define an asynchronous function to execute a single tool
async def execute_tool(tool_call: dict) -> tuple[str, Any]:
    """Execute a single tool asynchronously.

    Args:
        tool_call: Dictionary with tool execution details
    Returns:
        Tuple of tool ID and result/error
    """
    try:
        # If the tool is the mock tool, call it directly
        if tool_call["tool_name"] == "mock_tool":
            result = mock_tool(tool_call["args"].get("query", "mock query"))
            return tool_call["id"], result["results"]["mock_tool"]  # Return the mock result
        # Otherwise, execute the Tavily tool in a separate thread
        else:
            result = await asyncio.to_thread(  # Use asyncio.to_thread to run the synchronous tool in a separate thread
                tavily_tool.invoke,  # The synchronous tool to execute
                tool_call["args"]  # The arguments to the tool
            )
            return tool_call["id"], result[0]  # Return the result
    except Exception as e:  # Handle any exceptions during tool execution
        return tool_call["id"], f"Error: {str(e)}"  # Return the error message


# Example usage of the execute_tool function
async def example():
    # Define a tool call for the mock tool
    tool_call = {
        "id": "mock_1",
        "tool_name": "mock_tool",
        "args": {"query": "test"}
    }
    # Execute the tool asynchronously and get the result
    tool_id, result = await execute_tool(tool_call)
    # Print the tool ID and the result
    print(f"{tool_id}: {result}")  # Output: mock_1: mock_value

# Run the example function using asyncio.run(example())