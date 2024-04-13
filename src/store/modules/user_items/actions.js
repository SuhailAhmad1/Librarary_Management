export default {
    async loadItems(context, payload) {
        if (!payload.forceRefresh && !context.getters.shouldUpdate){
            return;
        }
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/user/get_all_items`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })
        const responseData = await response.json();

        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to fetch')
            throw error
        }
        context.commit('setItems', responseData.data)
        context.commit('setFetchTimeStamp')
    }
};