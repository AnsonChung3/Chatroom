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
        component: () => import("layouts/SolarizedDarkLayout.vue"),
        children: [
            { path: "", component: LoadPage("PageTemplate") },
            { path: "test", component: LoadPage("test") },
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
