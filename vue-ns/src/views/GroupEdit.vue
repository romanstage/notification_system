<template>
    <div>
        <v-row justify="center">
            <v-btn class="ma-2" small rounded color="teal darken-2" dark
                            @click="goBack"><v-icon
                                        class="mr-2"
                                      >
                                      mdi-account-multiple
                            </v-icon> Назад к группам </v-btn>
        </v-row>
        <v-row>


            <v-col cols="6">
                <ContactList
                    contactType='group-edit'
                    :isAddressBook="false"
                    mode="short"
                    v-on:emitAddContactToContactGroup="addContactToContactGroup"
                ></ContactList>
            </v-col>

            <v-col cols="6">
                <div>
                        <v-card
                                class=" mt-2"
                                max-width="800"
                                outlined
                                >
                            <v-row v-if="this.group">

                                <v-list-item three-line>
                                  <v-list-item-content>
                                  <v-row>
                                    <v-col cols="7">

                                    <h3 class="headline mb-1">{{group.title}}</h3>
<!--GROUP RENAME FORM-->

                                      <v-form v-if="showGroupRenameForm"
                                            ref="form"
                                            lazy-validation
                                              class="ma-2"
                                          >
                                          <v-divider ></v-divider>
                                            <v-text-field
                                            v-model="newGroupTitle"
                                            label="Введите новое название группы"
                                            outlined
                                            dense
                                            :counter="150"
                                            clearable
                                            ></v-text-field>
                                            <v-btn
                                              color="success"
                                              class="mr-4"
                                              @click="renameGroup(group_id_data)"
                                              small
                                              rounded
                                            >Сохранить
                                            </v-btn>

                                            <v-btn
                                              color="error"
                                              class="mr-4"
                                              @click="GroupRenameFormToggle"
                                              small
                                              rounded
                                            > Отмена
                                            </v-btn>
                                      </v-form>

<!--                                    <v-list-item-subtitle>Группа доступа: {{group.owner.name}}</v-list-item-subtitle>-->
                                    <v-list-item-subtitle>Количество абонентов: {{group.contact.length}}</v-list-item-subtitle>
                                  </v-col>
                                    <v-col cols="5">
                                        <v-card-actions>
                                            <v-row justify="end">
                                             <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                                          <v-btn class="mx-1 mr-2" fab dark x-small color="primary"
                  v-bind="attrs"
          v-on="on"
                   @click="GroupRenameFormToggle">

                <v-icon x-small dark>mdi-pencil</v-icon>
            </v-btn>
                         </template>
                     <span>Переименовать группу</span>
                 </v-tooltip>
                                                </v-row>
<!--                                          <v-btn @click="GroupRenameFormToggle" text>Переименовать</v-btn>-->
                                        </v-card-actions>
                                    </v-col>


                                  </v-row>
                                  </v-list-item-content>
                                </v-list-item>
                            </v-row>
                                      <v-divider></v-divider>
<!--                                    <v-row v-if="isGroup" v-for="contact in contacts" :key="contact.id">-->
<!--                                    <v-col cols="7">-->
<!--                                      {{contact.cn}}-->
<!--                                    </v-col>-->
<!--                                    <v-col cols="5">-->
<!--                                      <v-btn @click="removeContact(contact)"text>-->
<!--                                              <v-icon-->
<!--                                              class="mr-2"-->
<!--                                              >-->
<!--                                              mdi-arrow-left-bold-box-outline-->
<!--                                            </v-icon>-->
<!--                                         Удалить из списка</v-btn>-->
<!--                                    </v-col>-->

<!--                                  </v-row>-->


<!--                                  </v-list-item-content>-->
<!--                                </v-list-item>-->



<!--                        </v-row>-->


                              <v-data-table
                                v-if="isGroup"
                                :headers="headers"
                                :items="contacts"

                                hide-default-footer
                                class="elevation-1 ma-2"
                              >
                                  <template v-slot:item.actions="{ item }">
                                     <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">
                                              <v-icon
                                              class="mr-2"
                                              v-bind="attrs"
                                                v-on="on"
                                              @click="removeContact(item)"
                                              >
                                              mdi-arrow-left-bold-box-outline
                                            </v-icon>
                                         </template>
                     <span>Убрать из списока</span>
                 </v-tooltip>

                                  </template>
                              </v-data-table>


                    </v-card>

                </div>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import ContactList from "../components/Contacts/ContactList";

    export default {
        name: "GroupEdit",
        data() {
            return {
                group: null,
                contacts: null,
                isGroup: false,
                showGroupRenameForm: false,
                newGroupTitle: null,
                group_id_data: this.$route.params.group_id,
                 headers: [
                     { text: 'Действия', value: 'actions', sortable: false, align: 'start', },
                     {
                    text: 'ФИО',
                    align: 'start',
                    value: 'cn',
                  },
                  // { text: 'e-mail', value: 'mail' },
                  //{ text: 'Номер телефона', value: 'mobile_phone' },

                ],
            }
        },
      computed:{
      },
        components: {ContactList},
        props: {
            group_id: {
                type: Number
            }
        },
        methods: {
            getGroup(id) {
                // await

                this.$http(
                    `/contact/group/${id}/`)
                    .then(response => {


                        this.group = response.data;
                        this.isGroup = true
                        this.contacts = response.data.contact
                        console.log("GROUP RESULTS / this.group",this.group)
                        console.log("Contacts/ this.group.contact",this.contacts)
                        this.loading = false;
                    })
            },

            renameGroup(id){
                console.log('Renaming group with ID',id)

                this.$http.patch(`/contact/group/${id}/`,
                    {title: this.newGroupTitle},
                )
                .then((response) => {
                    if (response.status === 200) {
                        //Переименовывание группы во vue
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Группа "${this.group.title}" переименована в "${this.newGroupTitle}".`});
                        this.group.title = this.newGroupTitle
                        // this.$store.dispatch("alerts/addAlert", {
                        //'typeAlert': 'success', 'text': `Группа успешно переименована`});
                        console.log(response);
                        this.showGroupRenameForm = false

                    }
                    else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка переименования. ${response.status}: ${response.statusText}`});
                    }
                  })
                  .catch((error) => {
                    console.log(error);
                  })

            },

            GroupRenameFormToggle(){
                this.showGroupRenameForm = !this.showGroupRenameForm
            },

            addContactToContactGroup(ContactObject) {
              console.log("addContactToContactGroup fired", ContactObject)

              this.$http.patch(`/contact/edit-group/${this.group.id}`,
                    {contact_id:ContactObject.id},
                )
                .then((response) => {
                    if (response.status === 201) {
                        console.log(response);
                        this.addGroupModalShow = false;
                        //  Refresh for front update
                        this.getGroup(this.group_id_data);
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Контакт ${ContactObject.cn}  добавлен в  список "${this.group.title}".`});
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


            removeContact(ContactObject){
                console.log('Remove contact object', ContactObject)

                // console.log("OLD CONTACT LIST", this.contacts)
                const idx = this.contacts.indexOf(ContactObject)
                const newContactList = this.contacts.splice(idx, 1)
                // console.log("NEW CONTACT LIST", newContactList)

                // Axios.patch(`${this.$store.getters.getServerUrl}/contact/group/${this.group_id_data}`, options)
                // Axios.patch(`${this.$store.getters.getServerUrl}/contact/group/${this.group.id}/`,
                this.$http.delete(`/contact/edit-group/${this.group.id}`,
                    {data: {contact_id:ContactObject.id}},
                )
                .then((response) => {
                    if (response.status === 201) {
                        console.log(response);
                        this.addGroupModalShow = false
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Контакт ${ContactObject.cn}  удален из списока "${this.group.title}".`});
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
            goBack () {
                this.$router.push('/groups').catch(()=>{});
            },
        },

        mounted () {
             this.getGroup(this.group_id_data)
        },
    }



</script>

<style scoped>

</style>