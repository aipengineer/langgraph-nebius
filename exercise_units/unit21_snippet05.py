# Step 5: Complete Tool Pipeline
"""
Step 5: Complete Tool-Using Agent

Key Concepts:
- Full integration of all components
- Tool-enabled conversation flow
- State management across pipeline
"""
import json
import os
from typing import Annotated, Any, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import the TavilySearchResults tool from langchain_community.tools
from langchain_community.tools import TavilySearchResults
# Import StateGraph, START, and END from langgraph.graph
from langgraph.graph import StateGraph, START, END
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages


# Define the State class as before
class State(TypedDict):
    """Complete state for tool-using agent."""
    messages: Annotated[list[BaseMessage], add_messages]
    tool_calls: list[dict]
    tool_outputs: list[Any]


# Define the llm_node function as before
def llm_node(state: State) -> State:
    """Handle message processing and tool decisions."""
    # If there are no messages in the state, add a HumanMessage asking about the capital of France
    if not state.get("messages"):
        return {
            "messages": [HumanMessage(content="What is the capital of France?")],
            "tool_calls": [],
            "tool_outputs": []
        }

    # Get the content of the last message in the messages list
    last_message = state["messages"][-1].content
    # If the last message contains "capital of France", create a tool call to TavilySearchResults
    if "capital of France" in last_message:
        return {
            "tool_calls": [{
                "tool_name": "TavilySearchResults",
                "args": {"query": "capital of France"}
            }]
        }

    # Otherwise, return a new state with a thank you message
    return {
        "messages": [HumanMessage(content="Thanks for the information!")],
        "tool_calls": [],
        "tool_outputs": []
    }


# Define the tool_executor function as before
def tool_executor(state: State) -> State:
    """Execute tool calls."""
    # If there are no tool calls in the state, return an empty list of tool outputs
    if not state.get("tool_calls"):
        return {"tool_outputs": []}

    # Get the last tool call from the tool_calls list
    tool_call = state["tool_calls"][-1]
    # Create an instance of the TavilySearchResults tool
    tavily_tool = TavilySearchResults()

    try:
        # If the tool name is "TavilySearchResults", execute the tool with the given arguments
        if tool_call["tool_name"] == "TavilySearchResults":
            output = tavily_tool.invoke(tool_call["args"])
            # Return the tool output as a JSON string in the tool_outputs list
            return {"tool_outputs": [json.dumps(output)]}
    except Exception as e:
        # If there is an error during tool execution, return the error message as a JSON string
        return {"tool_outputs": [json.dumps({"error": str(e)})]}

    # Otherwise, return an empty list of tool outputs
    return {"tool_outputs": []}


# Define the result_processor function as before
def result_processor(state: State) -> State:
    """Process tool results into messages."""
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


# Define the should_end function as before
def should_end(state: State) -> bool:
    """Check if conversation should end."""
    # If there are no messages in the state, return False
    if not state.get("messages"):
        return False
    # Otherwise, check if the last message contains "Thanks for the information!"
    return "Thanks for the information!" in state["messages"][-1].content


# Create the complete graph
# Create a new StateGraph object
graph = StateGraph(State)

# Add nodes to the graph
graph.add_node("llm", llm_node)
graph.add_node("tool_executor", tool_executor)
graph.add_node("result_processor", result_processor)

# Connect nodes to define the flow of execution
graph.add_edge(START, "llm")
graph.add_edge("llm", "tool_executor")
graph.add_edge("tool_executor", "result_processor")
# Add conditional edges from "result_processor" to END or "llm" based on the should_end function
graph.add_conditional_edges(
    "result_processor",
    should_end,
    {True: END, False: "llm"}
)

# Compile the graph to make it ready for execution
chain = graph.compile()

# Example usage:
# Initialize the state and call the compiled graph with it
state = {
    "messages": [],
    "tool_calls": [],
    "tool_outputs": []
}
result = chain.invoke(state)