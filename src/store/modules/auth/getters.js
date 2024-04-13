export default {
    userId(state) {
        return state.userId;
    },
    token(state){
        return state.token;
    },
    isAuthenticated(){
        return !!localStorage.getItem("token");
    },
    getUserRole(state){
        return state.user_role;
    }
}
