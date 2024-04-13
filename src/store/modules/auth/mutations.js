export default{
    setUser(state, payload){
        state.token = payload.token;
        state.userId = payload.userId;
        state.user_role = payload.user_role;
    }
}