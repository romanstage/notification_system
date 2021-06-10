<template>
    <v-container>
        <v-dialog v-model="addGroupModalShow">
                <v-card>
                    <v-container fluid>
                        <v-row class="ma-2">
                            <v-col cols="4">
                                <v-form
                                    ref="form"
                                    lazy-validation
                                  >
                                    <v-text-field fluid
                                      v-model="newGroupTitle"
                                      :counter="50"
                                      label="Название группы!"
                                      required
                                    ></v-text-field>
                                    <v-btn
                                      color="success"
                                      class="mr-4"
                                      @click = "addGroup"
                                    >
                                      Сохранить
                                    </v-btn>
                                    <v-btn
                                      color="error"
                                      class="mr-4"
                                      @click = "addGroupModalShowToggle"

                                    >
                                      Отмена
                                    </v-btn>
                                  </v-form>
                            </v-col>
                        </v-row>
                </v-container>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script>
    export default {
        name: "deleteContactModal",
                computed: {

            deleteDialogOpend: {
                get() {
                    return this.$store.state.contactListModal.deleteModal.dialog;
                    console.log('get');
                },
                set(newVal){
                    if (!newVal) {
                    this.$store.dispatch("contactListModal/closeDialogDelete");
                    console.log('set');
                    }
                    return newVal
                }
            },

            deleteDialogContact: {
                get() {
                    return this.$store.state.contactListModal.deleteModal.contact;
                    console.log('get contact');
                },
            }
          },
    }

    <!-- МОДАЛ ДОБАВЛЕНИЯ НОВОЙ ГРУППЫ -->

</script>


<style scoped>

</style>