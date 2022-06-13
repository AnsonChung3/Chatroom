# views are what you call the endpoints
# these are only backend urls you'd want
from aiohttp import web
import motor.motor_asyncio
import os
from bson.objectid import ObjectId
import asyncio

# these fucntions are handling requests
# and if you look into routes.py, they are assigned a endpoint

# when to use async def?
# when it's attached to an endpoint

# -----------------------------------------------------
# golbal variables to be cleaned up before upload to remote
# only keeping client, db, collection
# -----------------------------------------------------
def setup_views():
    # this is not an endpoint
    # this is the init set up called in app.py
    # to init the database with default client, db, collection
    # and to set them as gobal variable that can be called from any def in views.py
    # new db and collections can be added with request from frontend
    global client, db, collection, chatrooms, messages
    connString = os.environ['MONGODB_CONNSTRING']
    client = motor.motor_asyncio.AsyncIOMotorClient(connString, connect=True)
    db = client.anson_database
    collection = db.anson_collection

    chatrooms = db.chatroom_collection
    messages = db.msg_collection

async def insert_many_msgs(request):
    body = await request.json()
    max = body['range']
    result = await collection.insert_many([{'x': i} for i in range(max)])
    return web.json_response(len(result.inserted_ids))

async def get_all_msg(request):
    result = do_find_all()
    return web.json_response(str(await result))

async def do_find_all():
    result = []
    async for doc in collection.find():
        result.append(doc)
    return result
    
async def find_many():
    result = []
    # cursor = collection.find()
    # cursor.sort('i', -1).skip(1).limit(2)
    async for doc in collection.find().sort('x', -1).limit(10):
        result.append(doc)
    return result

async def test_get_many_sort(request):
    result = await find_many()
    return web.json_response(str(result))

async def find_one(request):
    msg_id = request.match_info.get('msg_id', None)
    if msg_id is None:
        raise Exception("ID IS NONE AHHHHHHHHHHH!")
    # in collection.find_one()
    # {'_id': ObjectId(msg_id)}
    document = await messages.find_one({'_id': ObjectId(msg_id)})
    # document has to ber stringifyed before returning
    # otherwise it will give error 500, being document can't be json serilialized
    return web.json_response(str(document))

# let's try extracting all, without any filter
async def do_find(chatroom_id):
    list_of_msg = []
    async for msg in messages.find({'_id': ObjectId(chatroom_id)}):
        list_of_msg.append(msg)
    return list_of_msg

async def find_init_chat(id):
    result = []
    async for msg in messages.find( { "chatroomId": id } ).sort('timeStamp', 1).limit(100):
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result

async def init_chat(request):
    chatroomId = request.match_info.get('chatId', None)
    result = await find_init_chat(chatroomId)
    return web.json_response(result)

async def find_chatroom_msgs(id, timeStamp):
    result = []
    async for msg in messages.find( { "chatroomId": id, "timeStamp": { "$gt": timeStamp } } ).sort('timeStamp', -1).limit(100):
        msg["_id"] = str(msg["_id"])
        result.append(msg)
    return result

async def get_chatroom_msgs(request):
    chatroomId = request.match_info.get('chatroomId', None)
    timeStamp = int(request.match_info.get('timeStamp', None))
    result = await find_chatroom_msgs(chatroomId, timeStamp)
    return web.json_response(result)

async def send_msg(request):
    body = await request.json()
    document = body['document']
    result = await messages.insert_one(document)
    return web.json_response(str(result.inserted_id))

async def create_chatroom(request):
    body = await request.json()
    document = body['document']
    result = await chatrooms.insert_one(document)
    return web.json_response(str(result.inserted_id))

# this is the equivalent of prototype async def do_find() because the one for msg has filter/sort to it
async def find_chatrooms():
    list_of_chatrooms = []
    # chatrooms is the global variabel set at the start of the app
    async for chat in chatrooms.find():
        chat["_id"] = str(chat["_id"])
        list_of_chatrooms.append(chat)
    return list_of_chatrooms

async def get_chatrooms(request):
    result = find_chatrooms()
    return web.json_response(list(await result))