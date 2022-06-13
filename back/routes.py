import views

def setup_routes(app):
    app.router.add_route("GET", "/enter_chat/{chatId}", views.enter_chat)
    app.router.add_route("GET", "/get_msgs/{chatroomId}/{timeStamp}", views.get_chatroom_msgs)
    app.router.add_route("GET", "/get_chatrooms", views.get_chatrooms)
    app.router.add_route("POST", "/create_chatroom", views.create_chatroom)
    app.router.add_route("POST", "/send_msg", views.send_msg)
