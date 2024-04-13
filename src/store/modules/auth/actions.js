export default {
    async login(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/auth/login", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "email": payload.email,
                "password": payload.password
            })
        })

        const responseData = await response.json();
        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to login.')
            throw error;
        }

        localStorage.setItem('token', responseData.access_token);
        localStorage.setItem('user', responseData.user_id);
        localStorage.setItem("user_role", responseData.user_role)
        context.commit('setUser', {
            token: responseData.access_token,
            userId: responseData.user_id,
            user_role: responseData.user_role
        })

    },

    async signup(context, payload) {
        const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/auth/signup", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: payload.email,
                password: payload.password,
            })
        })

        const responseData = await response.json();

        if (!response.ok) {
            const error = new Error(responseData.message || 'Failed to signup.')
            throw error;
        }

        console.log(responseData)
    },

    async logout(context) {
        localStorage.removeItem("token")
        localStorage.removeItem("user")
        localStorage.removeItem("user_role")

        context.commit('setUser', {
            token: null,
            userId: null,
            user_role: null
        })
    }
}