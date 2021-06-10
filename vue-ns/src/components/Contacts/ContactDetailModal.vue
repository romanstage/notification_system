<template>
    <v-row justify="center">
         <v-dialog v-model="contactDetailModalOpend"  max-width="800">
                <v-card>

                    <v-container fluid v-if="contact.id">
                     <v-card-actions>
                                    <v-card-title>{{ contact.cn || 'Нет данных о Ф.И.О.'}}</v-card-title>
                                    <v-spacer></v-spacer>
                                    <v-btn class="mx-1" fab dark small color="red"  @click="contactDetailModalOpend=false, showMobileForm = false"> <v-icon dark>mdi-close</v-icon> </v-btn>
                     </v-card-actions>
                    <v-divider ></v-divider>
                        <v-row >
                            <v-col cols="4"
                                align="center"
                                justify="center"
                                    >
                                <v-img  v-if="contact.jpegPhoto!=''"
                                        :src="`${this.$backendURL}/static/userphoto/${contact.jpegPhoto}`"
                                        max-height="500"
                                        max-width="200"
                                    ></v-img>
                                <v-img  v-else
                                        :src="`${this.$backendURL}/static/userphoto/default.png`"
                                        max-height="500"
                                        max-width="200"
                                    ></v-img>

                            </v-col>
                            <v-col cols="8">
                                <v-container class='pa-5'>
                                <div><strong>Должность:</strong>{{ getDescription(contact.description || 'нет данных') }}</div>
                                <div><strong>Подразделение:</strong> {{ getCompanys(contact.company || 'нет данных') }}</div>
                                <div><strong>Aдрес:</strong> {{ contact.streetAddress || 'нет данных' }}</div>
                                <div><strong>e-mail:</strong> {{contact.mail || 'нет данных'}}</div>

<!--                                    <strong>Мобильный тел.:</strong> {{ this.currentMobile || 'нет данных'}}-->


                                <div><strong>Внутренниий телефон:</strong> {{ contact.pager || 'нет данных'}}</div>
                                <div><strong>Руководитель:</strong> {{getManager(contact)}}</div>
                                </v-container>
                            </v-col>
                        </v-row>
                        <v-divider ></v-divider>
                        <v-card-actions>
                                <v-card-title>Мобильные номера</v-card-title>
                                <v-spacer></v-spacer>
                                <v-btn  fab dark x-small color="green" small dark @click="showMobileForm = !showMobileForm"> <v-icon dark>mdi-plus</v-icon> </v-btn>
                        </v-card-actions>
                        <v-divider ></v-divider>
                        <v-row align="start"   justify="center" >
                                      <MobilePhoneForm v-if="showMobileForm"
                                    v-on:emitNewMobilePhone="addMobile"
                                    v-on:closeMobileForm="showMobileForm = !showMobileForm"
                                    />
</v-row>
                        <div v-if="contact.mobile_phone.length != 0">


<v-row align="start"   justify="center">
    <v-col class="col-9">
                            <template>

  <v-data-table
    :headers="headers"
    :items="contact.mobile_phone"
    dark
    dense
    hide-default-footer

    class="elevation-1"
  >
      <template v-slot:item.mobile="{ item }">
        {{ formatNumber(item.mobile)}}
      </template>
      <template v-slot:item.status="{ item }">
          <v-row>
            <v-checkbox @change="updateStatusMobilePhone(item)" dark v-model="item.status" :label="item.status ? 'Активен' : 'Отключен' "></v-checkbox>

              <v-tooltip v-if="item.telegram_id" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-icon class="ml-2"
                  color="primary"
                  dark
                  v-bind="attrs"
                  v-on="on"
                >mdi-telegram</v-icon>
              </template>
              <span>Доступна отправка сообщений в Telegram</span>
    </v-tooltip>
          </v-row>
      </template>
      <template v-slot:item.actions="{ item }">

          <v-icon @click="deleteMobilePhone(item)"> mdi-delete</v-icon>
      </template>
  </v-data-table>
</template>
        </v-col>
</v-row>




                        </div>






                </v-container>
            </v-card>
        </v-dialog>
    </v-row>
</template>



<script>
import MobilePhoneForm from './MobilePhoneForm'
    export default {
        name: "ContactDetailModal",
        props: {
            newMobile: {
                type: String
            },

        },
         data() {
            return {
            selection: 1,
            headers: [
                  {
                    text: 'Номер',
                    align: 'start',
                    value: 'mobile',
                  },
                {
                    text: 'Статус',
                    align: 'start',
                    value: 'status',
                  },

                  { text: 'Действия', value: 'actions', sortable: false, align: 'end', },
                ],

            dialog: false,
            currentMobile: null,
            newMobilePhone: null,
            showMobileForm: false,
            }
        },
            computed: {
                contactDetailModalOpend: {
                    get() {
                        console.log('get');
                        return this.$store.state.contactDetailModal.detailModal.dialog;
                        console.log('get');
                    },
                    set(newVal){
                        if (!newVal) {
                        this.$store.dispatch("contactDetailModal/closeDialogDetail");
                        console.log('set');
                        }
                        return newVal
                    }
                },
                contact : {
                    get() {
                        console.log('get contact');
                        console.log(this.$store.state.contactDetailModal.detailModal.contact);
                        return this.$store.state.contactDetailModal.detailModal.contact;
                    }
                }
          },
            components: {
            MobilePhoneForm,
        },

        methods: {
            formatNumber(number) {
                return `+7(${number.toString().substring(1,4)})${number.toString().substring(4, 7)}-${number.toString().substring(7, 9)}-${number.toString().substring(9, 11)}`
            },
            getCompanys(data) {
                // console.log('format company')
                console.log(data)
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

                    // Create a new array with only the first 5 items
                    // console.log(items.slice(0, 5));
                    items.slice(3,).forEach(e => arr.push(e[1]['value']))
                    return arr.join(' -> ');

            },
            getDescription (descriptionObj){
                let descriptionStr = '';
                for (const element of descriptionObj) {
                  descriptionStr += `${element.description} `;
                }
                return descriptionStr
            },


            getManager (user){
              if(user == null){
                  return ''
              }
                if (user.manager == null){
                    return 'нет данных'
                }
                return user.manager.cn
            },
            addMobile(newMobile){
                    console.log('AddMobileStart')
                    const data = {
                        "mobile": newMobile,
                        "status": true,
                        "telegram_id": null,
                        "user": this.contact.id
                    };


                    this.$http.post(`/contact/mobile-phone/`, data, )
                    .then((response) => {
                        if (response.status === 201) {
                            this.$store.dispatch("contactDetailModal/addPhoneNumber", response.data);
                            this.$store.dispatch("alerts/addAlert",
                                    {'typeAlert': 'success', 'text': `Номер ${newMobile} добавлен.`});
                        }
                        else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка добавления. ${response.status}: ${response.statusText}`});
                        }
                      })
                      .catch((error) => {
                        console.log(error);
                      })

                    this.showMobileForm = false
            },
            updateStatusMobilePhone(item){
                    console.log('updateStatusMobilePhone')
                    const data = {
                        "id": item.id,
                        "mobile": item.mobile,
                        "status": item.status,
                        "telegram_id": item.telegram_id,
                        "user": this.contact.id
                    };

                    console.log(item.status);
                    this.$http.patch(`/contact/mobile-phone/${item.id}/`, data, )
                    .then((response) => {
                        if (response.status === 200) {
                            // this.$store.dispatch("contactDetailModal/addPhoneNumber", response.data);
                            this.$store.dispatch("alerts/addAlert",
                                    {'typeAlert': 'success', 'text': `Статус номера ${item.mobile} обновлен.`});
                        }
                        else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка изменения статуса. ${response.status}: ${response.statusText}`});
                        }
                      })
                      .catch((error) => {
                        console.log(error);
                      })

                    this.showMobileForm = false
            },
            deleteMobilePhone(mobilePhoneObj){
              console.log('Delete phone with ID',mobilePhoneObj)

                    this.$http.delete(`/contact/mobile-phone/${mobilePhoneObj.id}/`, { params: mobilePhoneObj })
                    .then((response) => {
                        if (response.status === 204) {
                            this.$store.dispatch("contactDetailModal/removePhoneNumber", mobilePhoneObj);
                            this.$store.dispatch("alerts/addAlert",
                                    {'typeAlert': 'success', 'text': `Номер ${mobilePhoneObj.mobile} удален.`});
                        }
                        else {
                            this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Ошибка удаления. ${response.status}: ${response.statusText}`});
                        }
                      })
                      .catch((error) => {
                        console.log(error);
                      })

                    // this.showMobileForm = false
            }
        },
    }
</script>

<style scoped>
.prof_image {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px;
  width: 150px;
    image-orientation: from-image;
}
</style>