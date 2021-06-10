<template>
    <v-row justify="center">
        <v-dialog
      v-model="dialog"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">{{ message.title }}</v-card-title>

        <v-card-text>
            {{ message.message }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="orange darken-1"
            dark
            small
            @click="cancel"
          >
            {{ message.cancelMessage || 'Отмена' }}
          </v-btn>

          <v-btn
            color="red darken-1"
            dark
            small
            @click="confirm"
          >
              {{ message.confirmMessage || 'Да' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
    export default {
        name: "confirmDialog",
        computed: {

            dialog: {
                get() {
                    console.log('get');
                    return this.$store.state.dialog.confirmDialog.dialog;

                },
                set(newVal){
                    if (!newVal) {
                    this.$store.dispatch("dialog/closeDialog");
                    console.log('set');
                    }
                    return newVal
                }
            },

            message: {
                get() {
                    console.log('get message');
                    return this.$store.state.dialog.confirmDialog.message;

                },
            }
        },
        methods: {
            confirm() {
                this.$emit('confirm', {confirm: true, onSubmit: this.message.onSubmit });
                this.dialog = false;


                 console.log('EMITTTTTTTTTTTTTT');
            },
            cancel() {
                this.$emit('confirm', {confirm: false, onSubmit: this.message.onSubmit });
                this.dialog = false;

                 console.log('EMITTTTTTTTTTTTTT');
            }
        }

    }
</script>

<style scoped>

</style>