function LoadPage(component) {
    return () => import(`src/pages/${component}.vue`);
};

const routes = [
    {
        path: "/",
        component: () => import("layouts/MainLayout.vue"),
        children: [
            { path: "", component: LoadPage("Index") }
        ]
    },
    {
        path: "/template",
        component: () => import("layouts/chatroomLayout.vue"),
        children: [
            { path: "", component: LoadPage("PageTemplate") },
            { path: "chatroom", component: LoadPage("chatroom") }
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
