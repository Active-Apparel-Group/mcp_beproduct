#!/usr/bin/env python3
"""
MCP BeProduct Server

A Model Context Protocol server that provides tools and resources for 
Active Apparel Group product management operations.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    GetPromptRequest,
    GetPromptResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    CallToolRequest,
    CallToolResult,
    ReadResourceRequest,
    ReadResourceResult,
    TextContent,
    TextResourceContents,
    Tool,
    Prompt,
    Resource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server instance
server = Server("mcp-beproduct")


@server.list_resources()
async def handle_list_resources() -> ListResourcesResult:
    """List available resources"""
    resources = [
        Resource(
            uri="product://catalog",
            name="Product Catalog",
            description="Access to the Active Apparel Group product catalog",
            mimeType="application/json"
        ),
        Resource(
            uri="product://inventory", 
            name="Inventory Status",
            description="Current inventory levels and stock information",
            mimeType="application/json"
        ),
    ]
    return ListResourcesResult(resources=resources)


@server.read_resource()
async def handle_read_resource(request: ReadResourceRequest) -> ReadResourceResult:
    """Read a specific resource"""
    
    uri_str = str(request.params.uri)
    
    if uri_str == "product://catalog":
        # Mock product catalog data
        catalog_data = {
            "products": [
                {
                    "id": "AAG001",
                    "name": "Performance Athletic Shirt",
                    "category": "Activewear",
                    "price": 49.99,
                    "description": "Moisture-wicking athletic shirt perfect for workouts",
                    "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
                    "colors": ["Black", "Navy", "Gray", "Red"]
                },
                {
                    "id": "AAG002", 
                    "name": "Yoga Leggings",
                    "category": "Activewear",
                    "price": 69.99,
                    "description": "High-waisted compression leggings with side pockets",
                    "sizes": ["XS", "S", "M", "L", "XL"],
                    "colors": ["Black", "Navy", "Charcoal", "Purple"]
                },
                {
                    "id": "AAG003",
                    "name": "Running Shorts",
                    "category": "Activewear", 
                    "price": 39.99,
                    "description": "Lightweight 5-inch inseam running shorts with liner",
                    "sizes": ["S", "M", "L", "XL", "XXL"],
                    "colors": ["Black", "Navy", "Royal Blue", "Green"]
                }
            ]
        }
        
        return ReadResourceResult(
            contents=[
                TextResourceContents(
                    uri=request.params.uri,
                    mimeType="application/json",
                    text=str(catalog_data)
                )
            ]
        )
    
    elif uri_str == "product://inventory":
        # Mock inventory data
        inventory_data = {
            "inventory": [
                {"product_id": "AAG001", "total_stock": 150, "available": 120, "reserved": 30},
                {"product_id": "AAG002", "total_stock": 89, "available": 75, "reserved": 14},  
                {"product_id": "AAG003", "total_stock": 200, "available": 180, "reserved": 20}
            ],
            "last_updated": "2024-01-15T10:30:00Z"
        }
        
        return ReadResourceResult(
            contents=[
                TextResourceContents(
                    uri=request.params.uri,
                    mimeType="application/json",
                    text=str(inventory_data)
                )
            ]
        )
    
    else:
        raise ValueError(f"Unknown resource: {uri_str}")


@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools"""
    tools = [
        Tool(
            name="search_products",
            description="Search for products in the catalog by name, category, or other criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for products"
                    },
                    "category": {
                        "type": "string", 
                        "description": "Filter by product category",
                        "enum": ["Activewear", "Casual", "Outerwear"]
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price filter"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_inventory",
            description="Check inventory levels for a specific product",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID to check inventory for"
                    }
                },
                "required": ["product_id"]
            }
        ),
        Tool(
            name="update_product", 
            description="Update product information in the catalog",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {
                        "type": "string",
                        "description": "Product ID to update"
                    },
                    "updates": {
                        "type": "object",
                        "description": "Fields to update",
                        "properties": {
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "description": {"type": "string"}
                        }
                    }
                },
                "required": ["product_id", "updates"]
            }
        )
    ]
    return ListToolsResult(tools=tools)


@server.call_tool()
async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
    """Handle tool calls"""
    
    if request.params.name == "search_products":
        query = request.params.arguments.get("query", "")
        category = request.params.arguments.get("category")
        max_price = request.params.arguments.get("max_price")
        
        # Mock search functionality
        all_products = [
            {
                "id": "AAG001",
                "name": "Performance Athletic Shirt", 
                "category": "Activewear",
                "price": 49.99,
                "description": "Moisture-wicking athletic shirt perfect for workouts"
            },
            {
                "id": "AAG002",
                "name": "Yoga Leggings",
                "category": "Activewear", 
                "price": 69.99,
                "description": "High-waisted compression leggings with side pockets"
            },
            {
                "id": "AAG003",
                "name": "Running Shorts",
                "category": "Activewear",
                "price": 39.99, 
                "description": "Lightweight 5-inch inseam running shorts with liner"
            }
        ]
        
        # Filter products based on search criteria
        results = []
        for product in all_products:
            # Search in name and description
            if query.lower() in product["name"].lower() or query.lower() in product["description"].lower():
                # Apply category filter if specified
                if category and product["category"] != category:
                    continue
                # Apply price filter if specified
                if max_price and product["price"] > max_price:
                    continue
                results.append(product)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Found {len(results)} products matching your search:\n" + 
                         "\n".join([f"- {p['name']} (${p['price']}) - {p['description']}" for p in results])
                )
            ]
        )
    
    elif request.params.name == "check_inventory":
        product_id = request.params.arguments.get("product_id")
        
        # Mock inventory check
        inventory_map = {
            "AAG001": {"total_stock": 150, "available": 120, "reserved": 30},
            "AAG002": {"total_stock": 89, "available": 75, "reserved": 14},
            "AAG003": {"total_stock": 200, "available": 180, "reserved": 20}
        }
        
        if product_id in inventory_map:
            stock_info = inventory_map[product_id]
            return CallToolResult(
                content=[
                    TextContent(
                        type="text", 
                        text=f"Inventory for {product_id}:\n" +
                             f"Total Stock: {stock_info['total_stock']}\n" +
                             f"Available: {stock_info['available']}\n" +
                             f"Reserved: {stock_info['reserved']}"
                    )
                ]
            )
        else:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Product {product_id} not found in inventory system"
                    )
                ]
            )
    
    elif request.params.name == "update_product":
        product_id = request.params.arguments.get("product_id")
        updates = request.params.arguments.get("updates", {})
        
        # Mock update operation
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Successfully updated product {product_id} with the following changes: {updates}"
                )
            ]
        )
    
    else:
        raise ValueError(f"Unknown tool: {request.params.name}")


@server.list_prompts()
async def handle_list_prompts() -> ListPromptsResult:
    """List available prompts"""
    prompts = [
        Prompt(
            name="product_analysis",
            description="Analyze product performance and provide insights",
            arguments=[
                {
                    "name": "product_id", 
                    "description": "Product ID to analyze",
                    "required": True
                },
                {
                    "name": "timeframe",
                    "description": "Analysis timeframe (e.g., '30 days', '6 months')",
                    "required": False
                }
            ]
        ),
        Prompt(
            name="inventory_report", 
            description="Generate an inventory status report",
            arguments=[
                {
                    "name": "category",
                    "description": "Product category to focus on", 
                    "required": False
                }
            ]
        )
    ]
    return ListPromptsResult(prompts=prompts)


@server.get_prompt()
async def handle_get_prompt(request: GetPromptRequest) -> GetPromptResult:
    """Handle prompt requests"""
    
    if request.name == "product_analysis":
        product_id = request.arguments.get("product_id", "")
        timeframe = request.arguments.get("timeframe", "30 days")
        
        prompt_text = f"""
Please analyze the performance of product {product_id} over the last {timeframe}.

Consider the following aspects:
1. Sales performance and trends
2. Inventory turnover rates  
3. Customer feedback and reviews
4. Competitive positioning
5. Recommendations for optimization

Use the available product catalog and inventory data to provide specific insights.
"""
        
        return GetPromptResult(
            description=f"Product analysis for {product_id}",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text.strip()
                    }
                }
            ]
        )
    
    elif request.name == "inventory_report":
        category = request.arguments.get("category", "all categories")
        
        prompt_text = f"""
Generate a comprehensive inventory status report for {category}.

Include the following information:
1. Current stock levels for all products
2. Products with low stock warnings
3. Products with excess inventory
4. Recommended restocking actions
5. Seasonal trends and adjustments needed

Use the inventory data and product catalog to create actionable insights.
"""
        
        return GetPromptResult(
            description=f"Inventory report for {category}",
            messages=[
                {
                    "role": "user", 
                    "content": {
                        "type": "text",
                        "text": prompt_text.strip()
                    }
                }
            ]
        )
    
    else:
        raise ValueError(f"Unknown prompt: {request.name}")


def run_server():
    """Entry point for the server"""
    asyncio.run(main())


async def main():
    """Main entry point for the server"""
    # Import here to avoid issues with event loop
    from mcp.server.stdio import stdio_server
    from mcp.types import ServerCapabilities, ResourcesCapability, ToolsCapability, PromptsCapability
    
    logger.info("Starting MCP BeProduct server...")
    
    # Define server capabilities
    capabilities = ServerCapabilities(
        resources=ResourcesCapability(subscribe=False, listChanged=False),
        tools=ToolsCapability(listChanged=False),
        prompts=PromptsCapability(listChanged=False)
    )
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream,
            InitializationOptions(
                server_name="mcp-beproduct",
                server_version="0.1.0",
                capabilities=capabilities
            )
        )


if __name__ == "__main__":
    run_server()