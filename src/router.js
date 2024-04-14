import { createRouter, createWebHistory } from "vue-router";

import ItemList from "./pages/user_pages/ItemList.vue"
import AddRequest from "./pages/user_pages/AddRequest.vue"
import UserBooks from "./pages/user_pages/UserBooks.vue"
import UserRequests from "./pages/user_pages/UserRequests.vue"
import UserViewBook from "./pages/user_pages/UserViewBook.vue"
import NotFound from './pages/NotFound.vue';
import Test from './pages/Test.vue'
import ManagerItem from "./pages/manager_pages/ManagerItem.vue"
import EditItem from "./pages/manager_pages/EditItem.vue"
import AddItem from './pages/manager_pages/AddItem.vue'
import AddCategory from "./pages/manager_pages/AddCategory.vue"
import EditCategory from './pages/manager_pages/EditCategory.vue'
import ManUserRequests from './pages/manager_pages/ManUserRequests.vue'
import ManagerStatistics from './pages/manager_pages/ManagerStatistics.vue'
import ManagerRequests from './pages/manager_pages/ManagerRequests.vue'
import AdminRequests from './pages/admin_pages/AdminRequests.vue'
import ViewBook from './pages/manager_pages/ViewBook.vue'
import UserAuth from "./pages/auth/UserAuth.vue"
import store from './store/index.js'


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/test',
            component: Test        
        },
        {
            path: '/auth',
            component: UserAuth,
            meta: { requiresUnauth: true }
        },
        {
            path: "/",
            redirect: '/home',
            meta: { requiresAuth: true }
        },
        {
            path: '/home',
            component: ItemList,
            meta: { requiresAuth: true }
        },
        {
            path: '/books/:cat_id/add_to_request/:id',
            component: AddRequest,
            props: true,
            meta: { requiresAuth: true },
        },
        {
            path: '/my_books',
            component: UserBooks,
            meta: { requiresAuth: true }
        },
        {
            path: '/requests',
            component: UserRequests,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/view_book/:id',
            component: UserViewBook,
            props: true,
            meta: { requiresAuth: true }
        },
        

        // Manager Routes
        {
            path: '/home/manager',
            component: ManagerItem,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/addCategory',
            component: AddCategory,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/:cat_id/edit_category',
            component: EditCategory,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/:cat_id/edit/:id',
            component: EditItem,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/:id/addItem',
            component: AddItem,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/:id/view_book',
            component: ViewBook,
            props: true,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/user_requests',
            component: ManUserRequests,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/statistics',
            component: ManagerStatistics,
            meta: { requiresAuth: true }
        },
        {
            path: '/manager/requests',
            component: ManagerRequests,
            meta: { requiresAuth: true }
        },
        {
            path: '/admin/requests',
            component: AdminRequests,
            meta: { requiresAuth: true }
        },
        {
            path: '/:notFound(.*)',
            component: NotFound
        }
    ]
});

router.beforeEach(function (to, from, next) {
    if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
        next('/auth')
    } else if (to.meta.requiresUnauth && store.getters.isAuthenticated) {
        next("/home")
    }
    else {
        next()
    }
})

export default router;