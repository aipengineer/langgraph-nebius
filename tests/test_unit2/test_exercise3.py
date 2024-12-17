"""
Test suite for Exercise 2.3 - Parallel Tool Executor
"""

import logging
from typing import Any

import pytest
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_init_state_empty_input(student_submission: Any) -> None:
    """Test init_state with empty input."""
    try:
        init_state = student_submission.init_state
    except AttributeError:
        pytest.fail("Could not find init_state in student submission")

    result = init_state({})
    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["messages"][0].content == "Starting parallel tool execution..."
    assert len(result["pending_tools"]) == 2
    assert result["results"] == {}
    assert result["errors"] == {}


@pytest.mark.asyncio
async def test_init_state_with_input(student_submission: Any) -> None:
    """Test init_state with initial state."""
    try:
        init_state = student_submission.init_state
    except AttributeError:
        pytest.fail("Could not find init_state in student submission")

    input_state = {
        "messages": [HumanMessage(content="Initial message")],
        "pending_tools": [
            {
                "id": "search_custom",
                "tool_name": "TavilySearchResults",
                "args": {"query": "custom query"},
            }
        ],
        "results": {"existing_result": "some value"},
        "errors": {"existing_error": "some error"},
    }
    result = init_state(input_state)

    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["messages"][0].content == "Initial message"
    assert len(result["pending_tools"]) == 1
    assert result["pending_tools"][0]["id"] == "search_custom"
    assert result["results"] == {"existing_result": "some value"}
    assert result["errors"] == {"existing_error": "some error"}


@pytest.mark.asyncio
async def test_execute_tool_success(student_submission: Any) -> None:
    """Test execute_tool with a successful tool call."""
    try:
        execute_tool = student_submission.execute_tool
    except AttributeError:
        pytest.fail("Could not find execute_tool in student submission")

    tool_call = {
        "id": "search_success",
        "tool_name": "TavilySearchResults",
        "args": {"query": "successful query"},
    }
    tool_id, result = await execute_tool(tool_call)
    assert tool_id == "search_success"
    assert isinstance(result, dict)  # Assuming successful Tavily call returns a dict


@pytest.mark.asyncio
async def test_execute_tool_failure(student_submission: Any) -> None:
    """Test execute_tool with a failing tool call."""
    try:
        execute_tool = student_submission.execute_tool
    except AttributeError:
        pytest.fail("Could not find execute_tool in student submission")

    tool_call = {
        "id": "search_failure",
        "tool_name": "TavilySearchResults",
        "args": {},  # Invalid args to trigger error
    }
    tool_id, result = await execute_tool(tool_call)
    assert tool_id == "search_failure"
    assert isinstance(result, str)
    assert result.startswith("Error:")


@pytest.mark.asyncio
async def test_parallel_executor_no_tools(student_submission: Any) -> None:
    """Test parallel_executor with no pending tools."""
    try:
        parallel_executor = student_submission.parallel_executor
    except AttributeError:
        pytest.fail("Could not find parallel_executor in student submission")

    state = {
        "messages": [HumanMessage(content="No tools message")],
        "pending_tools": [],
        "results": {"pre_existing_result": "value"},
        "errors": {"pre_existing_error": "error_message"},
    }
    result = await parallel_executor(state)
    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["messages"][0].content == "No tools message"
    assert result["pending_tools"] == []
    assert result["results"] == {
        "pre_existing_result": "value",
        "mock_tool": "mock_value",
    }
    assert result["errors"] == {"pre_existing_error": "error_message"}


@pytest.mark.asyncio
async def test_parallel_executor_with_tools(student_submission: Any) -> None:
    """Test parallel_executor with pending tools."""
    try:
        parallel_executor = student_submission.parallel_executor
        get_initial_state = student_submission.get_initial_state
    except AttributeError:
        pytest.fail(
            "Could not find parallel_executor or get_initial_state in student submission"
        )

    result = await parallel_executor(get_initial_state())

    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["pending_tools"] == []
    assert len(result["results"]) == 2
    assert len(result["errors"]) == 0


@pytest.mark.asyncio
async def test_result_aggregator_no_results(student_submission: Any) -> None:
    """Test result_aggregator with no results."""
    try:
        result_aggregator = student_submission.result_aggregator
    except AttributeError:
        pytest.fail("Could not find result_aggregator in student submission")

    state = {"messages": [HumanMessage(content="Test message")], "results": {}}
    result = result_aggregator(state)
    assert result["messages"][0].content == "Test message"
    assert len(result["messages"]) == 1
    assert result["pending_tools"] == []
    assert result["results"] == {}
    assert result["errors"] == {}


@pytest.mark.asyncio
async def test_result_aggregator_with_results(student_submission: Any) -> None:
    """Test result_aggregator with results."""
    try:
        result_aggregator = student_submission.result_aggregator
    except AttributeError:
        pytest.fail("Could not find result_aggregator in student submission")

    state = {
        "messages": [HumanMessage(content="Test message")],
        "results": {
            "search_1": {"result1": "value1"},
            "search_2": {"result2": "value2"},
        },
    }
    result = result_aggregator(state)

    assert result["messages"][0].content == "Test message"
    assert len(result["messages"]) == 3
    assert result["pending_tools"] == []
    assert len(result["results"]) == 2
    assert result["errors"] == {}
    assert any("Result from search_1" in m.content for m in result["messages"])
    assert any("Result from search_2" in m.content for m in result["messages"])


@pytest.mark.asyncio
async def test_error_handler_no_errors(student_submission: Any) -> None:
    """Test error_handler with no errors."""
    try:
        error_handler = student_submission.error_handler
    except AttributeError:
        pytest.fail("Could not find error_handler in student submission")

    state = {"messages": [HumanMessage(content="Test message")], "errors": {}}
    result = error_handler(state)

    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["messages"][0].content == "Test message"
    assert len(result["messages"]) == 1
    assert result["pending_tools"] == []
    assert result["results"] == {}
    assert result["errors"] == {}


@pytest.mark.asyncio
async def test_error_handler_with_errors(student_submission: Any) -> None:
    """Test error_handler with errors."""
    try:
        error_handler = student_submission.error_handler
    except AttributeError:
        pytest.fail("Could not find error_handler in student submission")

    state = {
        "messages": [HumanMessage(content="Test message")],
        "errors": {"search_1": "Error message 1", "search_2": "Error message 2"},
    }
    result = error_handler(state)
    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert result["messages"][0].content == "Test message"
    assert len(result["messages"]) == 3
    assert result["pending_tools"] == []
    assert result["results"] == {}
    assert len(result["errors"]) == 2
    assert any("Error from search_1" in m.content for m in result["messages"])
    assert any("Error from search_2" in m.content for m in result["messages"])


@pytest.mark.asyncio
async def test_route_results_to_error_handler(student_submission: Any) -> None:
    """Test route_results with errors, should route to error_handler."""
    try:
        route_results = student_submission.route_results
    except AttributeError:
        pytest.fail("Could not find route_results in student submission")

    state = {"errors": {"some_error": "error message"}}
    result = route_results(state)
    assert result == "error_handler"


@pytest.mark.asyncio
async def test_route_results_to_result_aggregator(student_submission: Any) -> None:
    """Test route_results without errors, should route to result_aggregator."""
    try:
        route_results = student_submission.route_results
    except AttributeError:
        pytest.fail("Could not find route_results in student submission")

    state = {"results": {"some_result": "result message"}}
    result = route_results(state)
    assert result == "result_aggregator"


@pytest.mark.asyncio
async def test_graph_execution_with_empty_input(student_submission: Any) -> None:
    """Test the complete graph execution with empty input."""
    try:
        graph = student_submission.graph
    except AttributeError:
        pytest.fail("Could not find graph in student submission")

    # Provide minimal initial state
    initial_state = {
        "messages": [],  # Empty messages list but not None
        "pending_tools": [],  # Empty tools list but not None
        "results": {},  # Empty results dict but not None
        "errors": {},  # Empty errors dict but not None
    }

    result = await graph.ainvoke(initial_state)
    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert any("Mock tool called with query:" in m.content for m in result["messages"])
    assert len(result["messages"]) > 1
    assert result["pending_tools"] == []
    assert len(result["results"]) == 1
    assert len(result["errors"]) == 0


@pytest.mark.asyncio
async def test_graph_execution_with_initial_state(student_submission: Any) -> None:
    """Test the complete graph execution with initial state."""
    try:
        graph = student_submission.graph
        get_initial_state = student_submission.get_initial_state
    except AttributeError:
        pytest.fail("Could not find graph or get_initial_state in student submission")

    initial_state = get_initial_state()
    result = await graph.ainvoke(initial_state)

    assert isinstance(result, dict)
    assert "messages" in result
    assert "pending_tools" in result
    assert "results" in result
    assert "errors" in result
    assert len(result["messages"]) > 1
    assert result["pending_tools"] == []
    assert len(result["results"]) == 2
    assert len(result["errors"]) == 0
