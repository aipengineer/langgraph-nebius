# Step 5: Direct Tool Execution
"""
Step 5: Direct Tool Execution

Key Concepts:
- Tool invocation
- Parameter handling
- Result processing
"""
from typing import Annotated, Any, TypedDict
# Import the necessary message type from langchain_core.messages
from langchain_core.messages import BaseMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class with fields for direct tool execution
class State(TypedDict):
    """State for direct tool execution."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_name: str | None  # A field to store the selected tool name
    tool_outputs: list[str]  # A list to store tool execution results


# Define a function called execute_direct_tool that takes in the current state and a tool
# and returns an updated state with the tool execution result
def execute_direct_tool(state: State, tool: Any) -> State:
    """Execute a tool directly."""
    # If there is no tool name in the state, return an empty list of tool outputs
    if not state.get("tool_name"):
        return {**state, "tool_outputs": []}

    # Get the content of the last message in the messages list
    message = state["messages"][-1].content

    # Execute the tool based on the tool name
    if state["tool_name"] == "calculator":
        output = tool("2 + 2")  # Execute the calculator tool with a fixed expression
    elif state["tool_name"] == "check_weather":
        output = tool("Paris")  # Execute the check_weather tool with a fixed location
    else:
        output = "Tool not found"  # Return an error message if the tool is not found

    # Return an updated state with the tool output in the tool_outputs list
    return {**state, "tool_outputs": [output]}


# Example usage with calculator tool:
# Import the tool decorator from langchain_core.tools
from langchain_core.tools import tool


# Define a simple calculator tool using the @tool decorator
@tool
def simple_calc(expression: str) -> str:
    # Evaluate the expression using eval() and return the result as a string
    return str(eval(expression))


# Initialize the state with a tool name and call the execute_direct_tool function
state = {
    "messages": [],
    "tool_name": "calculator",
    "tool_outputs": []
}
result = execute_direct_tool(state, simple_calc)
# Print the first tool output from the result
print(result["tool_outputs"][0])  # Output: "4"