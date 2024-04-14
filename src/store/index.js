import { createStore } from "vuex";

import itemModule from './modules/user_items/index.js'
import cartModule from "./modules/cart/index.js"
import authModule from './modules/auth/index.js'
import managerModule from './modules/manager_items/index.js'
import adminModule from './modules/admin/index.js'

const store = createStore({
    modules: {
        items: itemModule,
        cart: cartModule,
        auth: authModule,
        manager_items: managerModule,
        admin_items: adminModule
    }
})

export default store;