import mutations from "./mutations"
import actions from "./actions"
import getters from "./getters"

export default({
    namespaced: true,
    state(){
        return {
            manager_requests: {
                "category_requests": [],
                "product_requests": []
            }
        }
    },
    mutations,
    actions,
    getters
})