export default({
    setItems(state, payload){
        state.manager_items = payload.data
    },
    addUserRequests(state, payload){
        state.user_requests = payload
    },
    addGraph(state, payload){
        state.graphUrl = payload
    },
    addBook(state, payload){
        state.bookUrl = payload
    },
    addRequests(state, payload){
        state.manager_requests = payload
    }
})