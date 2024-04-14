export default {
    addRequests(state, payload){
        state.cart_items = payload;
    },
    addBooks(state, payload){
        state.my_books = payload;
    },
    addBook(state, payload){
        state.bookUrl = payload
    }
};
