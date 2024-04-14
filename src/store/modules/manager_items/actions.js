export default ({
    async addCategory(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/add_category", {
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
            const error = new Error(responseData.message || 'Failed to add category.')
            throw error;
        }
    },

    async editCategory(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/edit_category", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                category_name: payload.category_name,
                category_id: payload.category_id,
                category_description: payload.category_description
            })
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to edit category.')
            throw error;
        }
    },

    async deleteCategory(context, payload) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/delete_category/${payload.id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to delete category.')
            throw error;
        }

        const response1 = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/get_all_products`, {
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

        context.commit('setItems', {
            data: responseData1.data
        })
    },

    async setAPIdata(context) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/get_all_products`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to get Items.')
            throw error;
        }

        context.commit('setItems', {
            data: responseData.data
        })

    },

    async editItem(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/edit_product", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "name": payload.itemName,
                "author": payload.author,
                "product_id": payload.id
            })
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to edit Items.')
            throw error;
        }
    },

    async addItem(context, payload) {
        const formData = new FormData();
        formData.append('file', payload.file);
        formData.append('name', payload.itemName);
        formData.append('author', payload.author);
        formData.append('category_id', payload.category_id)

        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/add_product", {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            },
            body: formData
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to add Item.')
            throw error;
        }
    },

    async deleteItem(context, payload) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/delete_product/${payload.id}`, {
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

        const response1 = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/get_all_products`, {
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

        context.commit('setItems', {
            data: responseData1.data
        })
    },

    async setUserRequestItems(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/get_alluser_requets", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to set order Items.')
            throw error;
        }
        context.commit('addUserRequests', responseData.data)
    },

    async updateRequestStatus(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/update_user_request_status", {
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
    },

    async setManagerGraph(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/get_statistics", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        if (!response.ok) {
            const error = new Error('Failed to get Graph Items.')
            throw error;
        }
        const responseData = await response.blob();

        context.commit('addGraph', URL.createObjectURL(responseData))
    },

    async setBookPdf(context, payload) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}/api/manager/get_book/${payload.id}`, {
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

    unsetBookPdf(context){
        context.commit("addBook", "")
    },

    async setRequestItems(context) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/get_manager_requests", {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem("token")}`
            }
        })

        if (!response.ok) {
            const error = new Error('Failed to get Graph Items.')
            throw error;
        }
        const responseData = await response.json();
        context.commit('addRequests', responseData.data)
    }
})