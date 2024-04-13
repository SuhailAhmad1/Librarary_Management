export default({
    managerItems(state){
        return state.manager_items;
    },

    hasItem(state){
        return state.manager_items.length !== 0;
    },
    managerOrders(state){
        return state.manager_orders
    },
    managerGraph(state){
        return state.graphUrl
    },
    managerRequests(state){
        return state.manager_requests;
    }
})