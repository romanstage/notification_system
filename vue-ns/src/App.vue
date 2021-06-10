<template>


    <v-app id="inspire">
        <v-navigation-drawer
                v-model="drawer"
                app
        >
            <v-list dense>
                <v-list-item @click="goHome" link>
                    <v-list-item-action>
                        <v-icon>mdi-home</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Главная</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>

                <v-list-item link>
                    <v-list-item-action>
                        <v-icon>mdi-account-tie-voice</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Голосовое оповещение</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                    <v-list-item-action>
                        <v-icon>mdi-email-send-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Текстовое оповещение</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>


                <v-list-item @click="goContacts" link>
                    <v-list-item-action>
                        <v-icon>mdi-contacts-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Контакты</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="goGroups" link>
                    <v-list-item-action>
                        <v-icon>mdi-account-group</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Группы</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item @click="goTemplates" link>
                    <v-list-item-action>
                        <v-icon>mdi-file-document-edit-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Шаблоны</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                    <v-list-item-action>
                        <v-icon>mdi-file-chart-outline</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Отчеты</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>


            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                app
                color="indigo"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>mGate 2.0</v-toolbar-title>
            <v-spacer></v-spacer>

            <v-btn icon>
                <v-icon>mdi-message-text</v-icon>
            </v-btn>

            <v-btn v-if="!loggedIn" @click="gologin" small color="primary">Войти</v-btn>
            <v-btn v-if="loggedIn" @click="logOut" small color="warning">Выход</v-btn>
        </v-app-bar>

        <v-main class="blue-grey lighten-5">


            <v-container
                    align="start"

                    fluid
            >

                <!-- здесь было выравнивание по высоте  -->
                <!--                <v-row  align="start"   justify="center"    >-->

                <router-view/>


                <!--                </v-row>-->
            </v-container>
        </v-main>

        <v-footer class="text-center"
                  color="indigo"
                  app
                  align="center"
                  justify="center"
        >

            <span class="white--text">*** "***"&copy; {{ new Date().getFullYear() }}</span>
        </v-footer>


          <v-snackbar
                    v-for="(alert, index) in alerts"
                    v-model="snackbar"
                    :key="index"
                    :timeout="-1"
                    :color="alert.typeAlert"
                    :style="`padding-bottom: ${(index * 60) + 8}px`"
                >
                     {{alert.text}}
                </v-snackbar>

    </v-app>

</template>

<script>
    import jwt_decode from "jwt-decode";

    export default {
        name: 'App',
        data: () => ({
            drawer: false,
            snackbar: true,
        }),
        components: {},
        computed: {
            loggedIn() {
                return this.$store.state.auth.status.loggedIn;
            },
            alerts: {
                get() {
                    return this.$store.state.alerts.alerts;
                },
            },
        },



        methods: {
            goHome() {
                this.drawer = false;
                this.$router.push({name: 'Home'}).catch(()=>{});

            },
            gologin() {
                this.$router.push({name: 'Auth'}).catch(()=>{});

            },
            logOut() {
                this.$store.dispatch('auth/logout');
                this.$router.push('/login').catch(()=>{});
            },
            goContacts() {
                this.drawer = false;
                this.$router.push('/contacts').catch(()=>{});
            },
            goGroups() {
                this.drawer = false;
                this.$router.push('/groups').catch(()=>{});
            },
            goTemplates() {
                this.drawer = false;
                this.$router.push('/templates').catch(()=>{});
            },

        },

    };
</script>

<style scoped>
    .alert-list {
        position: absolute;
        top: 0%;
        left: 0%;
      /*right: 200px;*/
        z-index: 7000;
    }
</style>
