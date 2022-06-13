import views
import demo_views

def setup_routes(app):
    app.router.add_route("GET", "/template/test", demo_views.test)
    # app.router.add_route("GET", "/find_one/{msg_id}", views.find_one)
    app.router.add_route("GET", "/init_chat/{chatId}", views.init_chat)
    app.router.add_route("GET", "/get_msgs/{chatroomId}/{timeStamp}", views.get_chatroom_msgs)
    app.router.add_route("GET", "/get_chatrooms", views.get_chatrooms)
    app.router.add_route("POST", "/create_chatroom", views.create_chatroom)
    app.router.add_route("POST", "/send_msg", views.send_msg)
