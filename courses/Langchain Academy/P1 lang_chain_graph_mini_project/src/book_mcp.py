from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from utility import get_book_details


OPENLIBRARY_BASE_URL = 'https://openlibrary.org/search.json'

app = Server('book-server')

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Define available tools for MCP server,

    Returns:
        list[Tool]: list of available tools
    """
    return [
        Tool(
            name='get_books',
            description='Gets details about the book, provides the top 5 search results from opnebooks api',
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Name of the book to search for"
                    }
                },
                "required": ["title"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Handle Tool execution

    Args:
        name: 
        arguments: 

    Returns:
        list[TextContent]: 
    """
    if name != 'get_books':
        raise ValueError(f'Unknown tool name: {name}')
    
    book_title = arguments['title']

    if not book_title:
        return [TextContent(type='text', text='Error: Book title is required')]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                OPENLIBRARY_BASE_URL,
                params={
                    'title': book_title
                }
            )
            response.raise_for_status()
            data = response.json()

        return [TextContent(type='text', text=get_book_details(book_data=data))]
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return [TextContent(type='text', text=f'Error: Book {book_title} not found')]
        return [TextContent(type='text', text=f'Error: API request failed with {e.response.status_code} code')]
    except Exception as e:
        return [TextContent(type='text', text=f'Error: Fetching weather data: {str(e)}')]

async def main():
    """Run MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == '__main__':
    asyncio.run(main())