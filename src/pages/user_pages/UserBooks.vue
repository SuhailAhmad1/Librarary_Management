<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h2>Current Books</h2>
        <table>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Expirey Date</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(book, index) in get_my_books['current']" :key="book.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ book.book_name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.expirey_at }}</td>
                    <td class="actions">
                        <base-button link :to="'/view_book/' + book.book_id">View</base-button>
                        <base-button mode="red" @click="returnBook(book.id)">Return</base-button>
                    </td>
                </tr>
            </tbody>
        </table>
    </section>
    <section>
        <h2>Completed / Returned Books</h2>
        <table>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Expirey Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(book, index) in get_my_books['completed']" :key="book.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ book.book_name }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.expirey_at }}</td>
                    <td v-if="book.is_returned" id="return">Returned</td>
                    <td v-else id="expired">Expired</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import TheHeader from '../../components/layout/TheHeader.vue'
export default {
    components: {
        TheHeader
    },
    data() {
        return {
            isLoading: false,
            error: null,
            openDropdowns: []
        };
    },
    methods: {
        async returnBook(id) {
            try {
                await this.$store.dispatch('cart/returnBook', {
                    request_id: id
                })
            } catch (err) {
                this.error = err.message || "Failed to load"
            }

            try {
                await this.$store.dispatch('cart/setMyBooks');
            } catch (err) {
                this.error = err.message || "Failed to load"
            }
        },
        closeError() {
            this.error = null;
        }
    },
    computed: {
        get_my_books() {
            return this.$store.getters['cart/my_books'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('cart/setMyBooks');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
#expired{
    background-color: #640054;
}
#return {
    background-color: #be7200;
}

section {
    padding: 2rem;
    margin: 3rem;
    background-color: rgb(23, 16, 37);
    border-radius: 1rem;
}

.placed_status {
    background-color: rgb(34, 12, 114);
}

.shipped_status {
    background-color: rgb(0, 92, 121);
}

.delivered_status {
    background-color: rgb(0, 110, 15);
}

.cancel_status {
    background-color: rgb(141, 0, 0);
}

header {
    text-align: center;
}

ul {
    list-style: none;
    margin: 2rem auto;
    padding: 0;
    max-width: 30rem;
}

h3,h2,
h5 {
    text-align: center;
}

.actions {
    margin: auto;
    max-width: 100px;
}

table {
    width: 95%;
    margin: 20px auto;
    text-align: center;
    border-collapse: collapse;
}

th {
    padding: 1.0rem;
    font-size: 1rem;
    font-weight: bold;
    border: 0.2px solid rgb(79, 100, 90);
    background-color: #00503c;
}

td {
    padding: 0.8rem;
    font-size: 0.7rem;
    border: 1px solid #384747;
}

.dropdown {
    position: relative;
    display: inline-block;
}

ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    border: 1px solid #ccc;
    background-color: #413838;
    position: absolute;
    left: 80%;
    z-index: 1;
}

li {
    padding: 8px;
    cursor: pointer;
}

li:hover {
    background-color: #161515;
}
</style>