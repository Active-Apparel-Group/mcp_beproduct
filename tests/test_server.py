"""Tests for MCP BeProduct server"""

import pytest
import asyncio
from mcp_beproduct.server import server


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_list_resources():
    """Test that resources are listed correctly"""
    result = await server.list_resources()()
    
    assert len(result.resources) == 2
    assert any(r.uri == "product://catalog" for r in result.resources)
    assert any(r.uri == "product://inventory" for r in result.resources)


@pytest.mark.asyncio
async def test_list_tools():
    """Test that tools are listed correctly"""
    result = await server.list_tools()()
    
    assert len(result.tools) == 3
    tool_names = [tool.name for tool in result.tools]
    assert "search_products" in tool_names
    assert "check_inventory" in tool_names
    assert "update_product" in tool_names


@pytest.mark.asyncio
async def test_list_prompts():
    """Test that prompts are listed correctly"""
    result = await server.list_prompts()()
    
    assert len(result.prompts) == 2
    prompt_names = [prompt.name for prompt in result.prompts]
    assert "product_analysis" in prompt_names
    assert "inventory_report" in prompt_names


@pytest.mark.asyncio
async def test_search_products_tool():
    """Test the search_products tool"""
    from mcp.types import CallToolRequest
    
    request = CallToolRequest(
        name="search_products",
        arguments={"query": "shirt"}
    )
    
    result = await server.call_tool()(request)
    
    assert len(result.content) == 1
    assert "Performance Athletic Shirt" in result.content[0].text


@pytest.mark.asyncio
async def test_check_inventory_tool():
    """Test the check_inventory tool"""
    from mcp.types import CallToolRequest
    
    request = CallToolRequest(
        name="check_inventory", 
        arguments={"product_id": "AAG001"}
    )
    
    result = await server.call_tool()(request)
    
    assert len(result.content) == 1
    assert "AAG001" in result.content[0].text
    assert "Available: 120" in result.content[0].text