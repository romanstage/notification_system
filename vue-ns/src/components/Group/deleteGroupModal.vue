<template>
    <v-row justify="center">
        <v-dialog
      v-model="deleteModal"
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">Удалить группу?</v-card-title>

        <v-card-text>
            Группа {{ deleteGroupModal.title }} будет удалена из вашего справочника.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="orange darken-1"
            dark
            small
            @click="deleteModal = false"
          >
            Отмена
          </v-btn>

          <v-btn
            color="red darken-1"
            dark
            small
            @click="deleteModal = false"
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
        name: "deleteGroupModal",
                computed: {
                      deleteModal: {
                          get() {
                              return this.$store.state.groupDeleteModal.deleteModal.dialog;
                              console.log('get');
                          },
                          set(newVal){
                              if (!newVal) {
                              this.$store.dispatch("groupDeleteModal/closeGroupDeleteModal");
                              console.log('set');
                              }
                              return newVal
                          }
                      },
          },
    }
</script>

<style scoped>

</style>