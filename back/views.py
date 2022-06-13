from aiohttp import web
import motor.motor_asyncio
import os
from bson.objectid import ObjectId
import asyncio

def setup_views():
    # this is not an endpoint
    # this is the init set up called in app.py
    # and to set gobal variable that can be called from any def in views.py
    # new db and collections can be added with request from frontend
    global client, db, chatrooms, messages
    connString = os.environ['MONGODB_CONNSTRING']
    client = motor.motor_asyncio.AsyncIOMotorClient(connString, connect=True)
    db = client.anson_database
    chatrooms = db.chatroom_collection
    messages = db.msg_collection

async def get_chatrooms(request):
    result = find_chatrooms()
    return web.json_response(list(await result))

async def find_chatrooms():
    list_of_chatrooms = []
    # chatrooms is the global variabel set at the start of the app
    async for chat in chatrooms.find():
        chat["_id"] = str(chat["_id"])
        list_of_chatrooms.append(chat)
    return list_of_chatrooms

async def create_chatroom(request):
    body = await request.json()
    document = body['document']
    result = await chatrooms.insert_one(document)
    return web.json_response(str(result.inserted_id))

async def enter_chat(request):
    chatroomId = request.match_info.get('chatId', None)
    result = await find_enter_chat(chatroomId)
    return web.json_response(result)

async def find_enter_chat(id):
    result = []
    async for msg in messages.find( { "chatroomId": id } ).sort('timeStamp', 1).limit(100):
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result

async def get_chatroom_msgs(request):
    chatroomId = request.match_info.get('chatroomId', None)
    timeStamp = int(request.match_info.get('timeStamp', None))
    result = await find_chatroom_msgs(chatroomId, timeStamp)
    return web.json_response(result)

async def find_chatroom_msgs(id, timeStamp):
    result = []
    async for msg in messages.find( { "chatroomId": id, "timeStamp": { "$gt": timeStamp } } ).sort('timeStamp', -1).limit(100):
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result

async def send_msg(request):
    body = await request.json()
    document = body['document']
    result = await messages.insert_one(document)
    return web.json_response(str(result.inserted_id))