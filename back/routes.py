from views import test

def setup_routes(app):
    app.router.add_route("GET", "/test", test)