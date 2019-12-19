from aiohttp import web
import importlib

app = web.Application()
routes = web.RouteTableDef()
# TODO: add autodiscover here
modules = ["server.handlers"]

def run_server(**kwargs):
    for module in modules:
        importlib.import_module(module)
    app.router.add_routes(routes)
    web.run_app(app, **kwargs)
    
