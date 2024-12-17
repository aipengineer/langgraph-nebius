# Step 5: Conditional Flow
"""
Step 5: Complete Conversation Flow

Key Concepts:
- Conditional edges control flow
- End conditions determine when to stop
- Full conversation cycle
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# Our state remains unchanged
class State(TypedDict):
    """Complete state definition."""
    messages: Annotated[list[BaseMessage], add_messages]


# Our node function is also mostly unchanged, except we have added a `response_map`
# to handle the conversational logic
def conversation_node(state: State) -> State:
    """Process messages in a simple conversational flow."""
    if not state["messages"]:
        return {"messages": [HumanMessage(content="Hello!")]}

    last_message = state["messages"][-1]
    # We've added this dictionary to handle the conversational logic
    # The keys are the expected messages, and the values are the responses
    response_map = {
        "Hello!": "How are you?",
        "How are you?": "Goodbye!"
    }

    # If the last message is in the response map, respond with the corresponding value.
    if last_message.content in response_map:
        return {"messages": [HumanMessage(content=response_map[last_message.content])]}
    # Otherwise, return the state unchanged.
    return state


# Define a function to determine whether to end the conversation.
# This function takes in the current state and returns a boolean value.
# We will add this function to our graph using `add_conditional_edges` below.
def should_end(state: State) -> bool:
    """Determine if we should end the conversation."""
    if not state["messages"]:
        return False
    # If the last message is "Goodbye!", then we should end the conversation.
    return state["messages"][-1].content == "Goodbye!"


# Create and compile the graph
graph = StateGraph(State)
graph.add_node("chat", conversation_node)
# Add "start" -> "chat" to specify the entry point in the graph
graph.add_edge(START, "chat")
# Add a conditional edge from "chat" to either END or "chat"
# The `should_end` function will be called whenever the "chat" node completes.
# If `should_end` returns True, the graph will transition to the END node.
# If `should_end` returns False, the graph will transition back to the "chat" node.
# The {True: END, False: "chat"} tells the graph how to interpret the output
# of the `should_end` function.
graph.add_conditional_edges(
    "chat",
    should_end,
    {
        True: END,
        False: "chat"
    }
)
# Compile the graph
chain = graph.compile()

# Example usage:
state = chain.invoke({"messages": []})
# Print the content of all messages in the state
print([msg.content for msg in state["messages"]])
# Output: ['Hello!', 'How are you?', 'Goodbye!']

