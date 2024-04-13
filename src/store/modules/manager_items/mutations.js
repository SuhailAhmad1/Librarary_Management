export default({
    setItems(state, payload){
        state.manager_items = payload.data
    },
    addToManagerOrders(state, payload){
        state.manager_orders = payload
    },
    addGraph(state, payload){
        state.graphUrl = payload
    },
    addRequests(state, payload){
        state.manager_requests = payload
    }
})