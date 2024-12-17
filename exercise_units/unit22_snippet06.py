# Step 6: ToolNode Execution
"""
Step 6: Using ToolNode

Key Concepts:
- ToolNode setup
- Tool configuration
- Message formatting
"""
from typing import Annotated, Any, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import AIMessage, BaseMessage
# Import the ToolNode class from langgraph.prebuilt
from langgraph.prebuilt import ToolNode
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class with fields for ToolNode execution
class State(TypedDict):
    """State for ToolNode execution."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_name: str | None  # A field to store the selected tool name
    tool_outputs: list[str]  # A list to store tool execution results


# Define a function called execute_with_tool_node that takes in the current state and a list of tools
# and returns an updated state with the tool execution result using ToolNode
def execute_with_tool_node(state: State, tools: list[Any]) -> State:
    """Execute tools using ToolNode."""
    # If there is no tool name in the state, return an empty list of tool outputs
    if not state.get("tool_name"):
        return {**state, "tool_outputs": []}

    # Create an instance of the ToolNode class with the given tools
    tool_node = ToolNode(tools)
    # Get the content of the last message in the messages list
    message = state["messages"][-1].content

    # Invoke the ToolNode with the message and tool code
    result = tool_node.invoke({
        "messages": [
            AIMessage(content=message,
                      tool_code=[{  # Specify the tool code for the selected tool
                          "name": state["tool_name"],
                          "args": {"query": message}  # Pass the message as an argument to the tool
                      }])
        ]
    })

    # Return an updated state with the tool output in the tool_outputs list
    return {**state, "tool_outputs": [result["messages"][0].content]}


# Example usage (simplified):
# Define the tools list with the check_weather tool from previous examples
tools = [check_weather]
# Initialize the state with a tool name and call the execute_with_tool_node function
state = {
    "messages": [],
    "tool_name": "check_weather",
    "tool_outputs": []
}
result = execute_with_tool_node(state, tools)
# Print the first tool output from the result
print(result["tool_outputs"][0])