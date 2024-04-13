export default ({
    async setRequestItems(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/admin/get_all_requests", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        if (!response.ok) {
            const error = new Error('Failed to Set Request Items.')
            throw error;
        }
        const responseData = await response.json();
        context.commit('addRequests', responseData.data)
    },

    async updateRequest(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/admin/update_request", {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        if (!response.ok) {
            const error = new Error('Failed to update request Items.')
            throw error;
        }
    }
})