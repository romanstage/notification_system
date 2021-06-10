<template>
    <v-row justify="center">
        <v-dialog
      v-model="genericModalToggle"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline"></v-card-title>

        <v-card-text>
          {{ message }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="orange darken-1"
            dark
            small
            v-on:click="genericModalToggle=false"
          >
            Отмена
          </v-btn>

          <v-btn
            color="red darken-1"
            dark
            small
            @click="confirm"
          >
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
    export default {
      name: "genericModal",
      props: {
        message: {
          type: String
        },
      },
      computed: {
        genericModalToggle: {
          get() {
            return this.$store.state.genericModal.genericModal.dialog;
            console.log('get');
          },
          set(newVal) {
            if (!newVal) {
              this.$store.dispatch("genericModal/closeGenericModal");
              console.log('set');
            }
            return newVal
          }
        },
      },
      methods:{
            confirm() {
            this.$emit('emitConfirm')
            this.$store.dispatch("genericModal/closeGenericModal");
          }
        },
    }
</script>

<style scoped>

</style>