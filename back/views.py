# views are what you call the endpoints
# these are only backend urls you'd want
from aiohttp import web

# these fucntions are handling requests
# and if you look into routes.py, they are assigned a endpoint
async def test(request):
    print ("getting into index")
    return web.Response(text='Hello Aiohttp!')
    