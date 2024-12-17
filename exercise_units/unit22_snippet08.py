# Step 8: Flow Control
"""
Step 8: Managing Conversation Flow

Key Concepts:
- Next step determination
- End conditions
- Flow branching
"""
from typing import Annotated, TypedDict, Literal
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages

# Define the State class with fields for flow control
class State(TypedDict):
    """State for result processing."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_outputs: list[str]  # A list to store tool execution results

# Define a function called get_next_step that takes in the current state
# and returns the name of the next step to execute
def get_next_step(state: State) -> Literal["tool_selector", "end"]:
    """Determine the next step in conversation flow."""
    # If there are no messages in the state, return "end"
    if not state.get("messages"):
        return "end"

    # Get the last message from the messages list
    last_message = state["messages"][-1]

    # End conditions
    # If the last message is a HumanMessage and contains "thanks" or "bye", return "end"
    if isinstance(last_message, HumanMessage):
        if any(word in last_message.content.lower()
               for word in ["thanks", "bye"]):
            return "end"

    # If the last message is an AIMessage and there are tool outputs, return "end"
    if isinstance(last_message, AIMessage) and state.get("tool_outputs"):
        return "end"

    # Otherwise, return "tool_selector" to continue the conversation
    return "tool_selector"

# Example usage:
# Initialize the state with a HumanMessage and call the get_next_step function
state = {
    "messages": [HumanMessage(content="thanks!")],
    "tool_outputs": []
}
next_step = get_next_step(state)
# Print the next step
print(next_step)  # Output: "end"