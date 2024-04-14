export default {
    request_items(state) {
        return state.cart_items;
    },
    my_books(state) {
        return state.my_books;
    },
    userBook(state){
        return state.bookUrl
    }
};