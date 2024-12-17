# Step 10: Complete Integration
"""
Step 10: Complete Multi-Tool Agent

Key Concepts:
- Full system integration
- State management
- Tool coordination
"""
from typing import Annotated, Any, NotRequired, TypedDict
# Import the necessary message types from langchain_core.messages
from langchain_core.messages import BaseMessage, HumanMessage
# Import END, START, and StateGraph from langgraph.graph
from langgraph.graph import END, START, StateGraph
# Import the ToolNode class from langgraph.prebuilt
from langgraph.prebuilt import ToolNode
# Import the add_messages function from langgraph.graph.message
from langgraph.graph.message import add_messages

# Reference to previously defined components
# Assuming these components are defined in a separate file called snippets.py
from snippets import (  # Normally from your implementation
    calculator,  # From Step 2: Basic Tool Definition
    check_weather,  # From Step 2: Basic Tool Definition
    tool_selector,  # From Step 4: Tool Selection
    execute_with_tool_node,  # From Step 6: ToolNode Execution
    result_processor,  # From Step 7: Result Processing
    get_next_step  # From Step 8: Flow Control
)


# Define the State class as before
class State(TypedDict, total=False):
    """Complete state for multi-tool agent."""
    messages: Annotated[list[BaseMessage], add_messages]
    available_tools: list[Any]  # A list to store the available tools
    tool_usage: dict[str, int]  # A dictionary to track tool usage
    rate_limits: dict[str, int]  # A dictionary to store tool rate limits
    tool_name: NotRequired[str | None]  # An optional field to store the currently selected tool name
    tool_outputs: NotRequired[list[str]]  # An optional field to store tool execution results


# Define a function called create_multi_tool_agent that creates and returns a complete multi-tool agent
def create_multi_tool_agent():
    """Create a complete multi-tool agent."""
    # Initialize tools
    tools = [calculator, check_weather]  # Create a list of available tools

    # Create graph
    graph = StateGraph(State)  # Create a new StateGraph object with the State defined earlier

    # Add nodes to the graph
    graph.add_node("tool_selector", tool_selector)  # Add the tool_selector function as a node
    # Add the execute_with_tool_node function as a node, using a lambda to pass the tools list
    graph.add_node("tool_executor",
                   lambda state: execute_with_tool_node(state, tools))
    graph.add_node("result_processor", result_processor)  # Add the result_processor function as a node

    # Add edges to connect the nodes in the graph
    graph.add_edge(START, "tool_selector")  # Connect the START node to the tool_selector node
    graph.add_edge("tool_selector", "tool_executor")  # Connect the tool_selector node to the tool_executor node
    graph.add_edge("tool_executor", "result_processor")  # Connect the tool_executor node to the result_processor node

    # Add conditional edges based on the get_next_step function
    graph.add_conditional_edges(
        "result_processor",  # Add conditional edges from the result_processor node
        get_next_step,  # Use the get_next_step function to determine the next step
        {
            "tool_selector": "tool_selector",  # If get_next_step returns "tool_selector", go to the tool_selector node
            "end": END  # If get_next_step returns "end", go to the END node
        }
    )

    # Return the compiled graph
    return graph.compile()


# Example usage:
# Call the create_multi_tool_agent function to create the agent and invoke it with an initial state
agent = create_multi_tool_agent()
result = agent.invoke({
    "messages": [HumanMessage(content="What's 2 + 2?")],  # Add an initial message
    "available_tools": [],
    "tool_usage": {},
    "rate_limits": {"calculator": 3}  # Set a rate limit for the calculator tool
})
# Print the content of the last message in the result
print(result["messages"][-1].content)