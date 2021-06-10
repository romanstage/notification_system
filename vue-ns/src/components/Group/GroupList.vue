<template>
    <v-container fluid>
                <v-row >
                    <v-col cols="3">
                        <v-text-field


                            hide-details
                            v-model="search"
                            label="Поиск"
                            prepend-inner-icon="mdi-magnify"
                            dense
                            outlined
                          ></v-text-field>
                </v-col>
                    <v-col cols="6"></v-col>
                        <v-col cols="3" align="end">



                            <v-btn class="ma-2" small rounded color="teal darken-3" dark
                            @click="addGroupModalShowToggle"><v-icon
                                        class="mr-2"
                                      >
                                      mdi-account-multiple-plus
                            </v-icon> Добавить группу </v-btn>




                    </v-col>
                </v-row>

<!-- Карточка группы (expantion model)     -->

    <v-expansion-panels
        inset
        focusable
    >
      <v-expansion-panel
        v-for="GroupObject in filteredList"
        :key="GroupObject.id"
        class="mb-1"

      >
        <v-expansion-panel-header>
          <v-row>
          <v-col align="start">
              <v-badge justify="left" inline :content="GroupObject.contact.length"><h3>{{GroupObject.title}}</h3></v-badge>
          </v-col>
          <v-col align="end" justify="right" >
            <v-tooltip top>
              <template v-slot:activator="{ on, attrs }">
                   <v-btn class="mx-1" fab dark x-small color="primary"
                  v-bind="attrs"
                    v-on="on"
                   @click="groupEdit(GroupObject.id)">
                    <v-icon x-small dark>mdi-pencil</v-icon>
                  </v-btn>
               </template>
                 <span>Редактирование группы</span>
           </v-tooltip>

            <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
            <v-btn class="mx-1" fab dark x-small color="red"
                   v-bind="attrs"
          v-on="on"
                   @click="openDeleteModal(GroupObject)">

                   <v-icon small dark>mdi-delete</v-icon>
            </v-btn>
                          </template>
                     <span>Удалить группу</span>
                 </v-tooltip>

          </v-col>
          </v-row>
        <template v-slot:actions>
            <v-icon color="primary">$expand</v-icon>
        </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-data-table

            :headers="headers"
            :items="GroupObject.contact"
            dense

            hide-default-footer
            class="elevation-6 mt-2"
          >
              <template v-slot:item.mobile_phone="{ item }">
                <v-row v-if="item.mobile_phone">
                <v-col v-for="mobile in item.mobile_phone" >
                {{ formatNumber(mobile)}}
                </v-col>
                    </v-row>
              </template>
          </v-data-table>

        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>


<!--      Модал подтверждения уделения группы-->
      <genericModal v-bind:message="this.message"
          v-on:emitConfirm="groupDelete"
        ></genericModal>
<!--  Модал добавления новой группы    -->

        <v-dialog v-model="addGroupModalShow" max-width="500">
                <v-card>
                    <v-container fluid>
                      <v-form
                          ref="form"
                          lazy-validation
                          class="ma-2"
                        >
                        <v-row>
                                    <v-text-field fluid
                                      v-model="newGroupTitle"
                                      :counter="50"
                                      label="Название группы"
                                      required
                                    ></v-text-field>

                          </v-row>
                          <v-row>

                                    <v-btn
                                      small
                                      color="success"
                                      class="mr-4"
                                      @click = "addGroup"
                                    >
                                      Сохранить
                                    </v-btn>
                                    <v-btn
                                      small
                                      color="error"
                                      class="mr-4"
                                      @click = "addGroupModalShow = false"

                                    >
                                      Отмена
                                    </v-btn>
                              </v-row>
                        </v-form>
                </v-container>
            </v-card>
        </v-dialog>
</v-container>

</template>

<script>
// import deleteGroupModal from "@/components/Group/deleteGroupModal";
import genericModal from "@/components/genericModal";


    export default {
        name: "GroupList",
         data() {
            return {
            search:'',
            groups:null,
            addGroupModalShow:false,
            deleteGroupModalShow:false,
            newGroupTitle:null,
            groupDeleteModalMessage:null,
            message:null,
            keyForMobile: 0,
            groupToDelete:null,
                headers: [{
                    text: 'ФИО',
                    align: 'start',
                    value: 'cn',
                  },
                  { text: 'e-mail', value: 'mail' },
                  { text: 'Номер телефона', value: 'mobile_phone' },
                ],
            }
        },
      components: {
          genericModal
      },
        methods:{
            getUniqueKey(id) {
                let uniqueKey = `${this.keyForMobile}${id}`;
                this.keyForMobile++;
                return uniqueKey
            },
            addGroupModalShowToggle(){
                  this.addGroupModalShow = !this.addGroupModalShow
              },

            addGroup(){
              this.addGroupModalShowToggle()
                console.log('Adding new group')

                this.$http.post(`/contact/add-contact-group/${this.newGroupTitle}`,)
                .then((response) => {
                console.log(response);
                    if (response.status === 200) {
                        this.addGroupModalShow = false;
                        this.getGroups();
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Группа ${this.newGroupTitle} добавлена.`});
                    }
                    else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка добавления. ${response.status}: ${response.statusText}`});
                    }
                  })
                  .catch((error) => {
                    console.log(error);
                  })
            },

            openDeleteModal (GroupObject) {
                   console.log('Generic GroupDeteleModal function fired ')
                    console.log(GroupObject)
                   let message = `Удалить группу  ${GroupObject.title}`
                   this.message = message
                   this.groupToDelete = GroupObject
                   // this.groupDeleteModalMessage = message
                   this.$store.dispatch("genericModal/openGenericModal", this.message);
                  // this.$store.dispatch("contactDetailModal/openDialogDetail", contact);

            },
            groupDelete(){
                let GroupObject = this.groupToDelete
                this.$http.delete(`/contact/group/${this.groupToDelete.id}/`,)
                .then((response) => {
                    //Удаление группы из vue
                    if (response.status === 204) {
                        const idx = this.groups.indexOf(this.groupToDelete)
                        this.groups.splice(idx, 1)
                        console.log(response);
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Группа ${GroupObject.title} удалена.`});
                    }
                    else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка удаления. ${response.status}: ${response.statusText}`});
                    }
                      })
                      .catch((error) => {
                        console.log(error);
                      })
            },
            groupEdit(id){
                console.log('Edit group with ID', id)
                this.$router.push({ name: 'GroupEdit', params: { group_id: id } })

            },

            getGroups() {
                   this.$http(
                        `/contact/group/`,
                    )
                        .then(response => {

                    console.log("GROUPS downloaded")
                    console.log(response.data.results)
                    this.groups = response.data.results;

                })
             },
            formatNumber(numberObj) {
                let number = numberObj.mobile
                return `+7(${number.toString().substring(1,4)})${number.toString().substring(4, 7)}-${number.toString().substring(7, 9)}-${number.toString().substring(9, 11)}`
            },
          },
         mounted () {
             this.getGroups()
        },
         computed: {
            filteredList() {
                if (this.groups != null){
                    return this.groups.filter(group => {
                        return group.title.toLowerCase().includes(this.search.toLowerCase())
              })
                }
            }
          }
    }
</script>

<style scoped>
.button{
display:inline-block;
  /*font-size: 20px;*/
}
.cen {
  background-color: #3366CC;
  display: flex;
  justify-content: center;
  align-content: center;
}
</style>