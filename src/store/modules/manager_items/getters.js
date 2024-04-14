export default({
    managerItems(state){
        return state.manager_items;
    },

    hasItem(state){
        return state.manager_items.length !== 0;
    },
    userRequests(state){
        return state.user_requests
    },
    managerGraph(state){
        return state.graphUrl
    },
    managerBook(state){
        return state.bookUrl
    },
    managerRequests(state){
        return state.manager_requests;
    }
})