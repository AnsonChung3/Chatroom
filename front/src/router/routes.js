function LoadPage(component) {
    return () => import(`src/pages/${component}.vue`);
};

const routes = [
    {
        path: "/",
        component: () => import("layouts/chatroomLayout.vue"),
        children: [
            { path: "", redirect: 'Chatroom' },
            { path: "Chatroom", component: LoadPage("chatroom") }
        ]
    },

    // Always leave this as last one,
    // but you can also remove it
    {
        path: "/:catchAll(.*)*",
        component: () => import("pages/Error404.vue")
    }
];

export default routes;
