from aiohttp import web
import aiohttp_cors
from routes import setup_routes
import motor.motor_asyncio
import views

# create a new aiohttp application
# this is responsible for all request related stuff
app = web.Application()
# this is responsible for adding the end point
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
    cors.add(route)

views.setup_views()

# start the aiohttp server
web.run_app(app)