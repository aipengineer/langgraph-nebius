# Step 4: Tool Selection Logic
"""
Step 4: Selecting Tools

Key Concepts:
- Message analysis
- Tool matching
- Selection criteria
"""
from typing import Annotated, Any, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class with fields for tool selection
class State(TypedDict):
    """State for tool selection."""
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]  # A list to store the available tools
    tool_name: str | None  # A field to store the selected tool name


# Define a node function called tool_selector that takes in the current state
# and returns an updated state with the selected tool name
def tool_selector(state: State) -> State:
    """Select appropriate tool based on message content."""
    # If there are no messages in the state, add a HumanMessage asking how to help
    if not state.get("messages"):
        return {
            **state,  # Keep the existing state
            "messages": [HumanMessage(content="How can I help you?")]  # Add a message asking how to help
        }

    # Get the content of the last message in the messages list and convert it to lowercase
    message = state["messages"][-1].content.lower()

    # Select the tool based on the message content
    if "weather" in message:
        return {**state,
                "tool_name": "check_weather"}  # Select the check_weather tool if the message contains "weather"
    elif any(word in message for word in ["calculate", "compute", "+", "-"]):
        return {**state,
                "tool_name": "calculator"}  # Select the calculator tool if the message contains math-related words
    else:
        return {**state, "tool_name": "search"}  # Otherwise, select the search tool


# Example usage:
# Initialize the state with a HumanMessage and call the tool_selector function
state = {
    "messages": [HumanMessage(content="What's the weather in Paris?")],
    "available_tools": [],
    "tool_name": None
}
result = tool_selector(state)
# Print the selected tool name
print(result["tool_name"])  # Output: "check_weather"