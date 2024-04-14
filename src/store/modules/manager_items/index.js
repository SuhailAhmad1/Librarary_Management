import mutations from "./mutations"
import actions from "./actions"
import getters from "./getters"

export default({
    namespaced: true,
    state(){
        return {
            lastFetch: null,
            manager_items: [],
            manager_orders: [],
            graphUrl: "",
            bookUrl: "",
            manager_requests: {}
        }
    },
    mutations,
    actions,
    getters
})