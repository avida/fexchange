from aiohttp import web
from server import routes
from  utils import logger

help_text = """
This is file upload server
"""

@routes.get("/")
async def handle(request):
    logger.info("Get event")
    return web.Response(text=help_text)

@routes.put("/{name}")
async def put_handle(request):
    logger.info("Put event")
    logger.info(f"{request.headers}")
    logger.info(f"{request.path}")
    async for chunk in request.content.iter_chunked(1024):
        logger.info(f"Chunk len is {len(chunk)}")
        print(chunk)
    return web.Response(text="Ok")
