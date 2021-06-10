<template>
    <div>

<!--   MODALS     -->
 <ContactDetailModal ></ContactDetailModal>

<!-- таблица -->
    <v-card>
        <v-row  class="ma-2">
            <v-chip v-for="filter in companyFilterButtons"
                    v-bind:key="filter.id"
                    v-bind:data="filter.company"
              class="ma-2"
              close small @click:close="removeCompanyFilter(filter)"
            >
                {{ filter.company }}
            </v-chip>
        </v-row>
            <v-card-title>

                <v-spacer>
                    <div v-if="!isAddressBook">Мои Контакты</div>
                    <div v-else>Справочник *** "***"</div>
                </v-spacer>
      <v-text-field
        v-model="options.search"
        append-icon="mdi-magnify"
        label="Поиск"
        single-line
        hide-details

      ></v-text-field>
    </v-card-title>




<!-- отключено нажатие на строку @click:row="handleClick" -->
    <v-data-table

     caption="Список контактов"
     :dark="dark"
     :multi-sort="multiSort"
    :headers="computedHeaders"
    :items="users"
    :options.sync="options"
    :server-items-length="totalUsers"
    :loading="loading"
    class="elevation-1 ma-2"
  >
        <template v-slot:item.company="{ item }">
          {{ getCompanys(item.company) }}
        </template>
        <template v-slot:item.description="{ item }">
          {{ getDescription(item.description) }}
        </template>

        <template v-slot:item.actions="{ item }">

              <v-row v-if="contactType === 'my-contacts'">
              <v-icon

                class="mr-2"
                @click="openUserDetail(item)"
              >
                mdi-card-account-details-outline
              </v-icon>
              <v-icon @click="deleteItem(item)"> mdi-delete </v-icon>
               </v-row>



                <v-row v-else-if="contactType === 'group-edit'">
                  <v-tooltip top>
                    <template v-slot:activator="{ on, attrs }">
                    <v-icon
                             v-bind="attrs"
          v-on="on"
                        class="mr-2"
                        @click="openUserDetail(item)"
                        >
                        mdi-card-account-details-outline
                    </v-icon>

                   </template>
                     <span>Подробная информация</span>
                 </v-tooltip>

                 <v-tooltip top>
      <template v-slot:activator="{ on, attrs }">

                    <v-icon
                             v-bind="attrs"
          v-on="on"
                          class="mr-2"
                          @click="emitAddContactToContactGroup(item) "
                          >
                          mdi-arrow-right-bold-box-outline
                      </v-icon>
      </template>
                     <span>Добавить в список</span>
                 </v-tooltip>
                </v-row>

              <v-row v-else-if="contactType === 'address-book'"><v-icon

                class="mr-2"
                @click="addItemToList(item)"
              >
               mdi-account-plus
              </v-icon>
              </v-row>

        </template>
</v-data-table>

    </v-card>

        <confirm-dialog @confirm = 'deleteContact'> </confirm-dialog>

    </div>
</template>

<script>
    import ContactDetailModal from "./ContactDetailModal";

    import ConfirmDialog from "../confirmDialog";

    export default {
        name: "ContactList",
        components: {ConfirmDialog, ContactDetailModal},
        props: {
            searchCompany: {
                type: Array
            },
            isAddressBook: {
              type: Boolean
            },
            contactType: {
                type: String
            },
            mode: {
                   type: String
            },
        },
        data() {
            return {
                dialogDeleteContact: false,
                searchStr: '',
                contactToDelete: null,
                ordering: '',
                companyFilter: '',
                companyFilterButtons: [],
                // table vars
                multiSort: true,
                dark: false,
                totalUsers: 0,
                users: [],
                loading: true,
                limit: 5,

                options: {
                    search: '',
                    itemsPerPage: 10,
                    page: 1,
                    sortBy: [],
                   // perPageOpt: [5,10,15,20,30,50,100,-1],
                },

                headers: [
                  {
                    text: 'ФИО',
                    align: 'start',
                    value: 'cn',
                  },
                  { text: 'Должность', value: 'description' },
                  { text: 'Подразделение', value: 'company',  sortable: false},
                  { text: 'Руководитель', value: 'manager.cn' },
                  { text: 'e-mail', value: 'mail' },
                  { text: 'Действия', value: 'actions', sortable: false, align: 'end', },
                ],
              }
        },
        computed:{
          computedHeaders () {
            var allHeaders = this.headers
            let filteredHeaders = []
            if (this.mode === 'full'){
              return allHeaders
            } else if (this.mode === 'short') {
              filteredHeaders = [
                  {
                    text: 'ФИО',
                    align: 'start',
                    value: 'cn',
                  },
                  { text: 'Должность', value: 'description' },
                  { text: 'Подразделение', value: 'company',  sortable: false},
                  { text: 'Действия', value: 'actions', sortable: false, align: 'end', },
                ]
              //   var filteredHeaders = allHeaders.filter(obj => {
              // return obj.essential === true
              // })
           }
            return filteredHeaders
        }
      },
        watch: {
            // 'deleteDialogOpend': {
            //     handler: function (newVal, oldVal) {
            //         console.log('wdwdqdqwd');
            //     }
            // },
            'isAddressBook': {
              handler: function (newVal, oldVal) {
                if (newVal != oldVal) {
                  console.log('page change');
                  console.log(oldVal);
                  console.log(newVal);
                  this.getDataFromApi();
                }

              }
            },
            'searchCompany': {
              handler: function (newVal, oldVal) {
                if (newVal != oldVal) {
                  console.log('page change');
                  console.log(oldVal);
                  console.log(newVal);
                  let filterIDs, filterStrings;
                  filterIDs = newVal.map(function (element) {
                        return element['id']
                  });
                  // filterStrings = newVal.map(function (element) {
                  //       return element['company']
                  // });
                  console.log('result');
                    console.log(filterIDs);
                    // console.log(filterStrings);
                   this.companyFilterButtons = newVal;
                  this.companyFilter = filterIDs.join();
                  this.getDataFromApi();
                }

              }
            },
            'options.page': {
                handler: function(newVal, oldVal) {
                if (newVal != oldVal) {
                    console.log('page change');
                     console.log(oldVal);
                     console.log(newVal);
                    this.getDataFromApi();
                    }
                },
                deep: true
            },
            'options.search': {
                handler: function(newVal, oldVal) {
                if (newVal != oldVal) {
                    console.log('search change');
                     console.log(oldVal);
                     console.log(newVal);
                    this.getDataFromApi();
                    }
                },
                deep: true
            },
            'options.itemsPerPage': {
                handler: function(newVal, oldVal) {
                if (newVal != oldVal) {
                    console.log('itemsPerPage change');
                     console.log(oldVal);
                     console.log(newVal);
                    this.getDataFromApi();
                    }
                },
                deep: true
            },
            'options.sortBy': {
                handler: function(newVal, oldVal) {
                if (newVal != oldVal) {
                    console.log('sortBy change');
                     console.log(oldVal);
                     console.log(newVal);
                    this.getDataFromApi();
                    }
                },
                deep: true
            },
        },

        mounted () {
            this.getUsers()
        },
        created() {
            //.then(data => { this.users})
        },
         methods: {
             handleClick(value) {
                 console.log(value);
             },
             removeCompanyFilter(element) {
                 let listCompany = this.companyFilterButtons;
                 listCompany = listCompany.filter(function (obj) {
                     return obj != element;
                 })
                 this.companyFilterButtons = listCompany;
                 this.$emit('remove-company-filter', listCompany);
             },

             addItemToList(item) {
                 if (!this.$store.state.auth.status.multiGroup) {
                     let group = this.$store.state.auth.user.groups[0];
                     this.$http.patch(`/contact/add_contact_to_my/${item.id}`,
                         {params: {id: item.id, available_to_groups: group.id}},)
                         .then(response => {
                             console.log(response);
                             if (response.status === 201) {
                                 this.$store.dispatch("alerts/addAlert",
                                     {'typeAlert': 'success', 'text': `Контакт ${item.cn} в ваш список.`});
                             } else {
                                 this.$store.dispatch("alerts/addAlert",
                                     {
                                         'typeAlert': 'danger',
                                         'text': `Ошибка добавления. ${response.status}: ${response.data.message}`
                                     });

                             }
                         })

                 } else {
                     this.$store.dispatch("alerts/addAlert",
                         {'typeAlert': 'danger', 'text': `У вас более одной группы! Обратитесь к Администратору.`});
                 }

             },
             deleteItem(contact) {
                 ///this.$store.dispatch("contactListModal/openDialogDelete", contact);
                 let message = {
                     title: "Удалить контакт",
                     message: `Вы хотите удалить контакт ${contact.cn}`,
                     confirmMessage: 'Удалить',
                     onSubmit: contact,
                 };
                 this.$store.dispatch("dialog/openDialog", message);
                 console.log(contact);
             },

             openUserDetail(contact) {
                 // this.contact_id = contact.id
                 this.$store.dispatch("contactDetailModal/openDialogDetail", contact);
             },

             deleteContact(answer) {
                 if (answer.confirm) {
                     console.log(`Confirm data ${answer.onSubmit}`)
                     console.log(answer)
                     if (!this.$store.state.auth.status.multiGroup) {
                         let group = this.$store.state.auth.user.groups[0];
                         this.$http.delete(`/contact/add_contact_to_my/${answer.onSubmit.id}`,
                             {params: {id: answer.onSubmit.id, available_to_groups: group.id}},)
                             .then(response => {
                                 console.log(response);
                                 if (response.status === 201) {
                                     this.$store.dispatch("alerts/addAlert",
                                         {'typeAlert': 'success', 'text': `Контакт ${answer.onSubmit.cn} удален.`});
                                     this.getDataFromApi();
                                 } else {
                                     this.$store.dispatch("alerts/addAlert",
                                         {
                                             'typeAlert': 'orange',
                                             'text': `Ошибка удаления. ${response.status}: ${response.data.message}`
                                         });

                                 }
                             })

                     } else {
                         this.$store.dispatch("alerts/addAlert",
                             {'typeAlert': 'orange', 'text': `У вас более одной группы! Обратитесь к Администратору.`});
                     }
                 } else {
                     console.log('Click cancel')
                 }
             },

             getCompanys(data) {
                 let arr = [];
                 var dict = []; // create an empty array
                 data.forEach(element => dict.push({
                     key: element.level,
                     value: element.company
                 }));
                 var items = Object.keys(dict).map(function (key) {
                     return [key, dict[key]];
                 });
                 // Sort the array based on the second element
                 items.sort(function (first, second) {
                     return second[1] - first[1];
                 });

                 // Create a new array with only the first 3 items
                 // console.log(items.slice(0, 5));
                 items.slice(3,).forEach(e => arr.push(e[1]['value']))
                 return arr.join(' -> ');

             },
             getDescription(descriptionObj) {
                 let descriptionStr = '';
                 for (const element of descriptionObj) {
                     descriptionStr += `${element.description} `;
                 }
                 return descriptionStr
             },
             getOrderString() {
                 let i;
                 let text = '';
                 let sortStr = '';
                 let sortElement;
                 for (i = 0; i < this.options.sortBy.length; i++) {
                     sortElement = this.options.sortBy[i];
                     switch (sortElement) {
                         case 'manager.cn':
                             sortStr = 'manager__cn';
                             break;
                         case 'description':
                             sortStr = 'description__description';
                             break;
                         default:
                             sortStr = sortElement;

                     }

                     text += this.options.sortDesc[i] ? `${sortStr},` : `-${sortStr},`;
                 }
                 this.ordering = text;

             },

             getDataFromApi() {
                 this.loading = true
                 return new Promise((resolve, reject) => {
                     const {sortBy, sortDesc, page, itemsPerPage} = this.options
                     console.log('STARTS GET FROM API')
                     this.getOrderString();
                     this.getUsers()
                     setTimeout(() => {
                         this.loading = false
                         resolve({
                             // items,
                         })
                     }, 1000)
                 })
             },
             // async
             getUsers() {
                 // await
                 this.$http.get(
                     `/contact/contact/`, {
                         headers: {Authorization: `JWT ${localStorage.getItem('access')}`,},
                         params: {
                             my: !this.isAddressBook,
                             page_size: this.options.itemsPerPage,
                             search: this.options.search,
                             ordering: this.ordering,
                             page: this.options.page,
                             company: this.companyFilter,
                             // ?page_size=${this.options.itemsPerPage}&search=${this.searchStr}&ordering=${this.ordering}
                         },
                         //}
                     }
                 )
                     .then(response => {
                         this.users = response.data.results;
                         this.totalUsers = response.data.total;
                         this.loading = false;
                         this.options.page = response.data.page
                     })
             },
             emitAddContactToContactGroup(item) {
              this.$emit('emitAddContactToContactGroup', item)
           }


    },
    }

</script>

<style scoped>

</style>