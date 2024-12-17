# Step 4: Result Processing
"""
Step 4: Processing Tool Results

Key Concepts:
- Handling tool outputs
- Converting results to messages
- Managing the conversation flow
"""
import json
from typing import Annotated, Any, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import StateGraph, START, and END from langgraph.graph
from langgraph.graph import StateGraph, START, END
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """State for result processing."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


# Define a node function called result_processor that takes in the current state
# and returns an updated state.
def result_processor(state: State) -> State:
    """Process and format tool results."""
    # If there are no tool outputs in the state, return an empty state
    if not state.get("tool_outputs"):
        return {
            "messages": [],
            "tool_calls": [],
            "tool_outputs": []
        }

    # Get the last tool output from the tool_outputs list
    tool_output = state["tool_outputs"][-1]
    # Return a new state with the tool output as a HumanMessage
    return {
        "messages": [HumanMessage(content=str(tool_output))],
        "tool_calls": [],
        "tool_outputs": []
    }


# Define a function called should_end that takes in the current state
# and returns a boolean indicating whether the conversation should end.
def should_end(state: State) -> bool:
    """Determine if we've completed the task."""
    # If there are no messages in the state, return False
    if not state.get("messages"):
        return False
    # Otherwise, check if the last message contains "Thanks for the information!"
    return "Thanks for the information!" in state["messages"][-1].content


# Create processing flow
# Create a new StateGraph object
graph = StateGraph(State)
# Add the result_processor function to the graph as a node named "processor"
graph.add_node("processor", result_processor)
# Add conditional edges from "processor" to END or "processor" based on the should_end function
graph.add_conditional_edges(
    "processor",
    should_end,
    {True: END, False: "processor"}
)

# Example usage:
# Initialize the state with a tool output and call the result_processor function
state = {
    "tool_outputs": [json.dumps({"result": "Paris is the capital of France"})],
    "messages": [],
    "tool_calls": []
}
result = result_processor(state)
# Print the content of the first message in the result
print(result["messages"][0].content)