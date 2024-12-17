# Step 2: Basic Tool Definition
"""
Step 2: Creating Tools

Key Concepts:
- Tool decorator
- Tool function structure
- Input/output handling
"""
# Import the tool decorator from langchain_core.tools
from langchain_core.tools import tool
# Import the numexpr and math libraries for mathematical calculations
import numexpr
import math


# Define a tool function called calculator using the @tool decorator
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate
    Returns:
        String representation of the result
    """
    # Create a local dictionary with predefined constants
    local_dict = {"pi": math.pi, "e": math.e}
    try:
        # Evaluate the mathematical expression using numexpr
        result = numexpr.evaluate(
            expression.strip(),
            global_dict={},
            local_dict=local_dict,
        )
        # Return the result as a string
        return str(float(result))
    except Exception as e:
        # If there is an error during evaluation, return the error message
        return f"Error evaluating expression: {e}"


# Define another tool function called check_weather using the @tool decorator
@tool
def check_weather(location: str) -> str:
    """Get weather for a location.

    Args:
        location: Name of the location
    Returns:
        Weather information
    """
    # Return a fixed weather message for the given location
    return f"It's always sunny in {location.strip()}"


# Example usage:
# Call the calculator tool with an expression and print the result
result = calculator("2 + 2")
print(result)  # Output: "4.0"
# Call the check_weather tool with a location and print the weather information
weather = check_weather("Paris")
print(weather)  # Output: "It's always sunny in Paris"