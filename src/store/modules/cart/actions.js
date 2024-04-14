export default {
    async addToRequest(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/add_to_requests", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to Add items in requests.')
            throw error;
        }
    },

    async setRequestItems(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/get_all_user_requests", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to get Cart Items.')
            throw error;
        }
        context.commit('addRequests', responseData.data)
    },

    async setMyBooks(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/get_my_books", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to get Cart Items.')
            throw error;
        }
        context.commit('addBooks', responseData.data)
    },

    async setBookPdf(context, payload) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/user/get_book/${payload.id}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        if (!response.ok) {
            const error = 'Failed to get Items.'
            this.error = error
        }

        const responseData = await response.blob();

        context.commit('addBook', URL.createObjectURL(responseData))
    },

    async returnBook(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/return_book/"+payload.request_id, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to update order status.')
            throw error;
        }
    }
};