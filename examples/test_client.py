#!/usr/bin/env python3
"""
Example client to test the MCP BeProduct server functionality.

This script demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
import json
from mcp_beproduct.server import handle_list_resources, handle_list_tools, handle_list_prompts, handle_read_resource, handle_call_tool


async def test_server_functionality():
    """Test various server capabilities"""
    
    print("=== MCP BeProduct Server Test ===\n")
    
    # Test listing resources
    print("1. Available Resources:")
    resources_result = await handle_list_resources()
    for resource in resources_result.resources:
        print(f"   - {resource.name}: {resource.uri}")
    print()
    
    # Test listing tools
    print("2. Available Tools:")
    tools_result = await handle_list_tools()
    for tool in tools_result.tools:
        print(f"   - {tool.name}: {tool.description}")
    print()
    
    # Test listing prompts
    print("3. Available Prompts:")
    prompts_result = await handle_list_prompts()
    for prompt in prompts_result.prompts:
        print(f"   - {prompt.name}: {prompt.description}")
    print()
    
    # Test reading a resource
    print("4. Reading Product Catalog Resource:")
    from mcp.types import ReadResourceRequest, ReadResourceRequestParams
    catalog_request = ReadResourceRequest(
        params=ReadResourceRequestParams(uri="product://catalog")
    )
    catalog_result = await handle_read_resource(catalog_request)
    print(f"   Content length: {len(catalog_result.contents[0].text)} characters")
    print("   Sample content:", catalog_result.contents[0].text[:200] + "...")
    print()
    
    # Test calling a tool
    print("5. Testing Search Products Tool:")
    from mcp.types import CallToolRequest, CallToolRequestParams
    search_request = CallToolRequest(
        params=CallToolRequestParams(
            name="search_products",
            arguments={"query": "shirt", "max_price": 50}
        )
    )
    search_result = await handle_call_tool(search_request)
    print("   Result:", search_result.content[0].text)
    print()
    
    # Test inventory check
    print("6. Testing Inventory Check Tool:")
    inventory_request = CallToolRequest(
        params=CallToolRequestParams(
            name="check_inventory",
            arguments={"product_id": "AAG002"}
        )
    )
    inventory_result = await handle_call_tool(inventory_request)
    print("   Result:", inventory_result.content[0].text)
    print()
    
    print("=== All tests completed successfully! ===")


if __name__ == "__main__":
    asyncio.run(test_server_functionality())