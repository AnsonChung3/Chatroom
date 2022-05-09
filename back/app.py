from aiohttp import web
import aiohttp_cors
from routes import setup_routes

# create a new aiohttp applcation
# this is responsible for all request related stuff
app = web.Application()
# this is responsible for adding the end point
# e.g. '/test'
setup_routes(app)

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    print (route)
    cors.add(route)

# start the aiohttp server
web.run_app(app)