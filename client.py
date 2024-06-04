"""
A simple HTTP/2 client which uses HTTP persistent connections.

This is a demo client demonstrating the issue with gevent based WSGI servers, when a
client tries to connect using HTTP/2 and persistent connections.
"""
import time
from aiohttp import ClientSession
import asyncio


async def main():
    """
    HTTP client trying to connect to the server using HTTP/2 upgrade and 
    persistent connections.
    """
    client = ClientSession(
        # Add the HTTP/2 Upgrade headers as described in RFC7540
        # (https://httpwg.org/specs/rfc7540.html#discover-http)
        headers= {
            "Connection": "Upgrade",
            "Upgrade": "h2c",  # Or h2 if using TLS
        },
    )
    async with client:
        while True:
            response = await client.post("http://127.0.0.1:8080", data="Hello, World!")
            if response.status == 200:
                print(await response.text())
            else:
                print(f"HTTP {response.status}: {response.reason}")

asyncio.run(main())
