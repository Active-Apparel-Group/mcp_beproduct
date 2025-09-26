# MCP BeProduct Server

A Model Context Protocol (MCP) server that provides tools and resources for Active Apparel Group product management operations.

## Features

- **Product Catalog**: Access to product information, descriptions, pricing, and availability
- **Inventory Management**: Real-time inventory tracking and stock level monitoring  
- **Search Tools**: Advanced product search with filtering capabilities
- **Analysis Prompts**: Pre-built prompts for product analysis and inventory reporting

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/Active-Apparel-Group/mcp_beproduct.git
cd mcp_beproduct
pip install -e .
```

### Install development dependencies

```bash
pip install -e .[dev]
```

## Usage

### Running the server

The MCP server can be started using the command line:

```bash
mcp-beproduct
```

Or run directly with Python:

```bash
python -m mcp_beproduct.server
```

### Integration with MCP clients

This server implements the Model Context Protocol and can be used with any MCP-compatible client. Configure your client to connect to this server using stdio transport.

Example configuration for Claude Desktop:

```json
{
  "mcpServers": {
    "mcp-beproduct": {
      "command": "mcp-beproduct",
      "args": []
    }
  }
}
```

## Available Resources

### Product Catalog (`product://catalog`)
Access to the complete product catalog with detailed information about each item including:
- Product IDs, names, and descriptions
- Pricing information
- Available sizes and colors
- Product categories

### Inventory Status (`product://inventory`)
Real-time inventory data including:
- Current stock levels
- Available vs reserved quantities
- Last updated timestamps

## Available Tools

### `search_products`
Search for products in the catalog by name, category, or other criteria.

**Parameters:**
- `query` (required): Search query string
- `category` (optional): Filter by product category
- `max_price` (optional): Maximum price filter

### `check_inventory`
Check inventory levels for a specific product.

**Parameters:**
- `product_id` (required): Product ID to check

### `update_product`
Update product information in the catalog.

**Parameters:**
- `product_id` (required): Product ID to update
- `updates` (required): Object containing fields to update

## Available Prompts

### `product_analysis`
Generate detailed analysis of product performance and provide insights.

**Arguments:**
- `product_id` (required): Product ID to analyze
- `timeframe` (optional): Analysis timeframe

### `inventory_report`
Generate comprehensive inventory status reports.

**Arguments:**
- `category` (optional): Product category to focus on

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black mcp_beproduct/
isort mcp_beproduct/
```

### Type checking

```bash
mypy mcp_beproduct/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Support

For support and questions, please open an issue on the GitHub repository.