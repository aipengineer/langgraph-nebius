# Step 4: Message Flow
"""
Step 4: Managing Message Flow

Key Concepts:
- Annotated types help LangGraph manage messages
- Messages can be added and processed
- State flows through nodes
"""
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
# Import the `add_messages` function
from langgraph.graph.message import add_messages


# Update our state to use the Annotated type
class State(TypedDict):
    """State with proper message handling annotation."""
    # The messages key is annotated with the `add_messages` function.
    # This tells LangGraph that whenever it receives an update to the `messages` key
    # that it should use this function to apply the update.
    # We'll see how this is used in the `conversation_node` function below.
    messages: Annotated[list[BaseMessage], add_messages]


# Update our node function to have a more complex conversation
def conversation_node(state: State) -> State:
    """A node that responds based on the last message."""
    # If there are no messages in the state, add a "Hello!" message.
    if not state["messages"]:
        return {"messages": [HumanMessage(content="Hello!")]}

    # Otherwise, get the last message
    last_message = state["messages"][-1]
    # And check its content
    if last_message.content == "Hello!":
        # If the content is "Hello!", respond with "How are you?"
        return {"messages": [HumanMessage(content="How are you?")]}
    # Otherwise, respond with "Goodbye!"
    return {"messages": [HumanMessage(content="Goodbye!")]}


# Create and compile the graph
graph = StateGraph(State)
# Add our node to the graph
graph.add_node("chat", conversation_node)
# The entry point is the chat node
graph.add_edge(START, "chat")
# We add a "chat" -> "chat" edge.
# This creates a cycle in our graph, meaning that every time the "chat" node
# completes, it will loop back to the "chat" node to continue processing.
# This is how we continue the conversation!
graph.add_edge("chat", "chat")  # Loop back to continue conversation
# Compile the graph
chain = graph.compile()

# Example usage:
# Invoke the graph
state = chain.invoke({"messages": []})
# Print out the content of all the messages in the state
print([msg.content for msg in state["messages"]])  # Output: ['Hello!']


