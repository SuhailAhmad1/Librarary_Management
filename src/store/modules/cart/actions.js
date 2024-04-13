export default {
    async addToCart(context, payload){
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/add_to_cart", {
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
            const error = new Error(responseData.message || 'Failed to Add items in a Cart.')
            throw error;
        }
    },

    async setCartItems(context,payload){
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/get_all_cart_items", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(payload)
        })
        
        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to get Cart Items.')
            throw error;
        }
        context.commit('addToCart', responseData.data)
    },

    async editCartItem(context, payload){
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/user/edit_cart_item", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "cart_id": payload.cart_id,
                "quantity": payload.quantity,
                "amount": payload.amount
            })
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to edit Items.')
            throw error;
        }
    },
    async deleteItem(context, payload) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/user/delete_cart_item/${payload.id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to delete Item.')
            throw error;
        }
        
        const response1 = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/user/get_all_cart_items`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        const responseData1 = await response1.json();
        if (!response.ok) {
            const error = new Error(responseData1.message || 'Failed to get Items.')
            throw error;
        }
        context.commit('addToCart', responseData1.data)
    }
};