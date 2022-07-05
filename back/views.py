from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
import os

def setup_views():
    # this is not an endpoint
    # this is the init set up called in app.py
    # and to set gobal variable that can be called from any def in views.py
    # new db and collections can be added with request from frontend but is not implemented for this project
    global client, db, chatrooms, messages
    connString = os.environ['MONGODB_CONNSTRING']
    client = AsyncIOMotorClient(connString, connect=True)
    db = client.anson_database
    chatrooms = db.chatroom_collection
    messages = db.msg_collection

async def get_chatrooms(request):
    result = do_find_chatrooms()
    return web.json_response(list(await result))

async def do_find_chatrooms():
    list_of_chatrooms = []
    # chatrooms is the global variable set at the start of the app
    async for room in chatrooms.find():
        room["_id"] = str(room["_id"])
        list_of_chatrooms.append(room)
    return list_of_chatrooms

async def create_chatroom(request):
    body = await request.json()
    document = body['document']
    result = await chatrooms.insert_one(document)
    return web.json_response(str(result.inserted_id))

async def get_msgs(request):
    chatroomId = request.match_info.get('chatroomId', None)
    # default value for timeStamp is set to 0 to request all result
    timeStamp = int(request.query.get('timeStamp', 0))
    result = await do_find_msgs(chatroomId, timeStamp)
    return web.json_response(result)

async def do_find_msgs(id, timeStamp):
    result = []
    async for msg in messages.find( { "chatroomId": id, "timeStamp": { "$gt": timeStamp } } ).sort('timeStamp', 1).limit(100):
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result

async def send_msg(request):
    body = await request.json()
    document = body['document']
    result = await messages.insert_one(document)
    return web.json_response(str(result.inserted_id))