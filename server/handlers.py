from aiohttp import web
from server import routes
from  utils import logger
from controllers import storage
from http import HTTPStatus

help_text = """
This is file upload server
"""

@routes.get("/")
async def handle(request):
    logger.info("Get event")
    return web.Response(text=help_text)

def get_dir_and_fname(request):
    return request.match_info.get('directory'), \
           request.match_info.get('filename')

@routes.get("/{directory}")
async def get_directory(request):
    directory, _ = get_dir_and_fname(request)
    resp_io = storage.get_directory(directory)
    if resp_io:
        logger.info(f"Sending {len(resp_io)} bytes")
        return web.Response(body=resp_io, headers={
            "Content-Disposition": f'attachment; filename="{directory}.zip"'
        })
    else:
        return web.Response(status=HTTPStatus.NOT_FOUND)

@routes.get("/{directory}/{filename}")
async def get_file(request):
    directory, filename = get_dir_and_fname(request)
    file_io = storage.get_file(directory, filename)
    if file_io:
        logger.info(f"Return file {len(file_io)}")
        return web.Response(body=file_io)
    else:
        return web.Response(status=HTTPStatus.NOT_FOUND)

@routes.put("/{filename}")
async def put_handle(request):
    directory, filename = get_dir_and_fname(request)
    directory = storage.new_directory()
    if directory is None:
        return web.Response(status=HTTPStatus.NO_CONTENT)
    return await upload_file(request, directory, filename)

@routes.put("/{directory}/{filename}")
async def put_handle(request):
    directory, filename = get_dir_and_fname(request)
    return await upload_file(request, directory, filename)

async def upload_file(request, directory, filename):
    logger.info("Upload event")
    peerinfo = request.transport.get_extra_info("peername")
    logger.info(f"{peerinfo}")
    await storage.save_file(filename, request.content, directory)
    return web.Response(text=f"dimar.pp.ua/{directory}/{filename}")
