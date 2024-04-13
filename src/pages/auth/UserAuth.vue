<template>
  <the-login-header></the-login-header>
  <base-dialog :show="!!error" title="Error occured" @close="closeError">
    <p>{{ error }}</p>
  </base-dialog>
  <base-dialog :show="isLoading" fixed :title="mode === 'login' ? 'Loging in...' : 'Signing up...'">
    <base-spinner></base-spinner>
  </base-dialog>
  <section>
    <base-card>
      <form @submit.prevent="submitForm">
        <div class="form-control">
          <label for="email">E-mail</label>
          <input type="email" id="email" v-model.trim="email" />
        </div>
        <div class="form-control">
          <label for="password">Password</label>
          <input type="password" id="password" v-model.trim="password" />
        </div>
        <p v-if="!formIsValid">Please check your inputs and try again!</p>
        <div class="actions">
          <base-button>{{ submitButtonCaption }}</base-button>
          <base-button type="button" mode="flat" @click="swithAuthMode">{{
    switchModeButtonCaption
            }}</base-button>
        </div>
      </form>
    </base-card>
  </section>
</template>

<script>
import TheLoginHeader from '../../components/layout/TheLoginHeader.vue';
export default {
  components: {
    TheLoginHeader
  },
  data() {
    return {
      email: '',
      password: '',
      formIsValid: true,
      mode: 'login',
      isLoading: false,
      error: null,
    };
  },
  computed: {
    submitButtonCaption() {
      if (this.mode === 'login') {
        return 'Login';
      }
      return 'Register';
    },
    switchModeButtonCaption() {
      if (this.mode === 'login') {
        return 'Register';
      }
      return 'Login';
    },
  },
  methods: {
    closeError() {
      this.error = null;
    },
    async submitForm() {
      this.formIsValid = true;
      if (
        this.email === '' ||
        !this.email.includes('@') ||
        this.password.length < 6
      ) {
        this.formIsValid = false;
        return;
      }

      this.isLoading = true;
      try {
        if (this.mode === 'signup') {
          await this.$store.dispatch('signup', {
            email: this.email,
            password: this.password,
          });
        } else {
          await this.$store.dispatch('login', {
            email: this.email,
            password: this.password,
          });
          const role = this.$store.getters['getUserRole']
          let redirectUrl;
          if (role == "manager") {
            redirectUrl = "/" + (this.$route.query.redirect || 'home/manager');
          }
          else if (role == "user") {
            redirectUrl = "/" + (this.$route.query.redirect || 'home');
          }
          else {
            redirectUrl = "/" + (this.$route.query.redirect || 'admin/requests');
          }
          this.$router.replace(redirectUrl);
        }
      } catch (err) {
        this.isLoading = false;
        this.error = err.message || 'Failed to signup, try again later!';
      }
      this.isLoading = false;
    },
    swithAuthMode() {
      if (this.mode === 'login') {
        this.mode = 'signup';
      } else {
        this.mode = 'login';
      }
    },
  },
};
</script>


<style scoped>
section {
  margin-top: 8rem;
}

form {
  margin: 3rem;
  padding: 1rem;
}

.form-control {
  margin: 0.5rem 0;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
}

input,
textarea {
  display: block;
  width: 100%;
  font: inherit;
  border: 1px solid #ccc;
  padding: 0.15rem;
}

input:focus,
textarea:focus {
  border-color: #3d008d;
  background-color: #faf6ff;
  outline: none;
}

.errors {
  font-weight: bold;
  color: red;
}

.actions {
  margin-top: 2rem;
  text-align: center;
}
</style>