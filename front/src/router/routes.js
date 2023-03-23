function LoadPage(component) {
    return () => import(`src/pages/${component}.vue`);
};

const routes = [
    {
        path: "/Chatroom",
        component: () => import("layouts/chatroomLayout.vue"),
        children: [
            { path: "", component: LoadPage("chatroom") }
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
