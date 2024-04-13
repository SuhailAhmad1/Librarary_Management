export default {
    setItems(state, payload){
        state.items = payload
    },
    setFetchTimeStamp(state){
        state.lastFetch = new Date().getTime();
    }
};