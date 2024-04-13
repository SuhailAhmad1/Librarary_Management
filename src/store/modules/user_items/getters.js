export default {
    items(state) {
        return state.items;
    },
    hasItems(state) {
        return state.items && state.items.length > 0;
    },  
    shouldUpdate(state) {
        const lastFetch = state.lastFetch
        if (!lastFetch) {
            return true
        }
        else {
            const currentTime = new Date().getTime();
            return (currentTime - lastFetch) / 1000 > 60;
        }
    }
};