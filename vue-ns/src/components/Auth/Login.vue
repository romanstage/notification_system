<template>
     <v-row class="justify-center">
         <v-col class="col-4">
                  <v-card class="elevation-12">
                <v-toolbar
                  color="primary"
                  dark
                  flat
                >
                  <v-toolbar-title>Вход в систему</v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-tooltip bottom>

                  </v-tooltip>
                </v-toolbar>
                <v-card-text>
                  <v-form name="form" @submit.prevent="handleLogin">
                    <v-text-field @keyup.enter.native="handleLogin"
                      label="Имя пользователя"
                      name="login"
                      v-model="user.username"

                      prepend-icon="mdi-account"
                      type="text"
                      required
                    ></v-text-field>

                    <v-text-field @keyup.enter.native="handleLogin"
                      id="password"
                      label="Пароль"
                      name="password"
                      v-model="user.password"
                      prepend-icon="mdi-lock"
                      type="password"
                      required
                    ></v-text-field>
                  </v-form>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" @click.prevent="handleLogin">войти</v-btn>
                </v-card-actions>
              </v-card>
             </v-col>
     </v-row>
</template>

<script>
    import User from '../../models/user';

    export default {
    name: 'Login',

  data() {
    return {
      user: new User('', ''),
      loading: false,
      message: ''
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    }
  },
  created() {
    if (this.loggedIn) {
      this.$router.push('/').catch(()=>{});
    }
  },
  methods: {
    handleLogin() {
      // this.loading = true;
      // this.$validator.validateAll().then(isValid => {
      //   if (!isValid) {
      //     this.loading = false;
      //     return;
      //   }

        if (this.user.username && this.user.password) {
          this.$store.dispatch('auth/login', this.user).then(
            () => {
              this.$router.push('/').catch(()=>{});
            },
            error => {
              this.loading = false;
              this.message =
                (error.response && error.response.data) ||
                error.message ||
                error.toString();
            }
          );
        }
      // });
    }
  }
};

</script>

<style scoped>

</style>