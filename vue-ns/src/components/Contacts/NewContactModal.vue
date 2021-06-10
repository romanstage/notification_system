<template>
  <v-dialog
      v-model="dialog"

    >
    <v-card>
        <v-card-title class="headline grey lighten-2">
          Новый контакт
        </v-card-title>

      <v-stepper v-model="e1">
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">Создать контакт</v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 2" step="2">Выбрать подразделение</v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step step="3">Добавить номера</v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1">
            <v-card
              class="mb-12"
            >
              <v-card-text>
          <v-container>
            <v-row>
              <v-col cols='12' sm="12" md="12">
                <v-checkbox
                  v-model="checkbox"
                  label='Сотрудник *** "***"'
                ></v-checkbox>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Фамилия*" required v-model="lastname"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Имя" hint=""
                  persistent-hint required v-model="firstname" ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Отчество"
                  v-model="midelname"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field label="Email*" required v-model="contact.email"></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small>*Обязательные поля</small>
        </v-card-text>
            </v-card>

            <v-btn
              color="primary"
              @click="goToStep2"
            >
              Подолжить
            </v-btn>

            <v-btn text @click="closeDialog">Отмена</v-btn>
          </v-stepper-content>

          <v-stepper-content step="2">
            <v-card
              class="mb-12"
            >
              <v-card-text>
                  <v-row justify="center">
                      <v-col cols="12" sm="6" md="6">
                        <v-text-field
                          label="Должность"
                          v-model="contact.description"
                          hint="Укажите должность"
                          persistent-hint
                        ></v-text-field>
              </v-col>
                  </v-row>
          <v-container v-if="checkbox">
<!--            <v-row>-->
              <CompanyTree
                selectionType="leaf"
                @search-company="selectCompany"
                :activeCompany="activeCompany"
              ></CompanyTree>
<!--            </v-row>-->
          </v-container>
          <v-container v-else>
            <v-row>
              <v-col cols="12" sm="6" md="6">
                <v-text-field label="Организация*" required v-model="contact.division"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field label="Подразделение" hint="" v-model="contact.department"
                  persistent-hint></v-text-field>
              </v-col>
<!--              <v-col cols="12" sm="6" md="4">-->
<!--                <v-text-field-->
<!--                  label="Должность"-->
<!--                ></v-text-field>-->
<!--              </v-col>-->
            </v-row>
          </v-container>

        </v-card-text>
            </v-card>

            <v-btn
              color="primary"
              @click="addContact"
            >
              Сохранить
            </v-btn>
            <v-btn text  @click="e1 = 1">Назад</v-btn>
            <v-btn text @click="closeDialog">Отмена</v-btn>
          </v-stepper-content>

          <v-stepper-content step="3">
            <v-card
              class="mb-12"
            >
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
                        <div>
                <v-row align="start"   justify="center">
                    <v-col class="col-9">
                                            <template>

                  <v-data-table
                    :headers="headers"
                    :items="storedMobile"
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
            </v-card>

            <v-btn
              color="primary"
              @click="closeDialog"
            >
              Закрыть
            </v-btn>

            <v-btn text @click="addAnotherContact">Добавить еще</v-btn>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
       <v-divider></v-divider>

<!--        <v-card-actions>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn-->
<!--            color="primary"-->
<!--            text-->
<!--            @click="dialog = false"-->
<!--          >-->
<!--            I accept-->
<!--          </v-btn>-->
<!--        </v-card-actions>-->
      </v-card>
    </v-dialog>
</template>

<script>
import MobilePhoneForm from './MobilePhoneForm'
  import CompanyTree from "./CompanyTree";

    export default {
        name: "NewContactModal",
        components: {CompanyTree,  MobilePhoneForm},
        data () {
          return {
            e1: 1,
            checkbox: true,
            midelname: '',
            firstname: '',
            lastname: '',
            activeCompany: [],
            contact : {
                id: null,
                cn: null,
                email: '',
                company: null,
                division: null, // организация
                department: null, // отдел
                description: null, // должность
            },

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
            currentMobile: null,
            newMobilePhone: null,
            showMobileForm: false,

          }
        },
        computed: {
                dialog: {
                    get() {
                        console.log('get');
                        return this.$store.state.createContactModal.createContact.dialog;
                        console.log('get');
                    },
                    set(newVal){
                        if (!newVal) {
                        this.$store.dispatch("createContactModal/closeDialogCreateContact");
                        console.log('set');
                        }
                        return newVal
                    },
                },
                storedMobile : {
                    get() {
                        console.log('get contact');
                        console.log(this.$store.state.createContactModal.createContact.contact.mobile_phone);
                        return this.$store.state.createContactModal.createContact.contact.mobile_phone;
                    }
                }
                // contact : {
                //     get() {
                //         console.log('get contact');
                //         console.log(this.$store.state.createContactModal.createContact.contact);
                //         return this.$store.state.createContactModal.createContact.contact;
                //     }
                // }
        },
        methods: {
          selectCompany(searchCompanyList) {
                this.contact.company = searchCompanyList;
          },
          validateEmail(email) {
              console.log(email);
              const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
              return re.test(email);
          },

          goToStep2() {
              console.log(this.lastname);
              console.log(this.contact.email);
              switch (true) {
                  case this.lastname != ''  && this.validateEmail(this.contact.email):
                      this.contact.cn = `${this.lastname} ${this.firstname} ${this.midelname}`
                      this.e1 = 2;
                      break;
                  case this.lastname == '':
                      this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Введите фамилию.`});
                  case this.contact.email == '':
                      this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Введите email.`});
                      break;
                  case !this.validateEmail(this.contact.email):
                      this.$store.dispatch("alerts/addAlert",
                                {'typeAlert': 'orange', 'text': `Не верный email.`});
              }
          },
          addContact() {
              console.log(this.contact);
              if (!this.$store.state.auth.status.multiGroup) {
                            let group = this.$store.state.auth.user.groups[0];
                            const data = {
                                'cn': this.contact.cn,
                                'mail': this.contact.email,
                                'company': this.contact.company,
                                'description': this.contact.description,
                                'division': this.contact.division,
                                'department': this.contact.department,
                            };
                            this.$http.post(`/contact/add_new_contact/`,
                                data,)
                                .then(response => {
                                    console.log(response);
                                    if (response.status === 201) {
                                        this.$store.dispatch("alerts/addAlert",
                                                {'typeAlert': 'success', 'text': `Контакт ${this.contact.cn} добавлен.`});
                                        this.contact.id = response.data.id;
                                        this.e1 = 3;
                                    }
                                    else {
                                        this.$store.dispatch("alerts/addAlert",
                                            {'typeAlert': 'orange', 'text': `Ошибка добавления. ${response.status}: ${response.data.message}`});

                                    }
                                })

                            }
                            else {
                              this.$store.dispatch("alerts/addAlert",
                                    {'typeAlert': 'orange', 'text': `У вас более одной группы! Обратитесь к Администратору.`});
                            }

          },
          clearForm () {
              this.contact = {
                id: null,
                cn: null,
                email: '',
                company: null,
                division: null, // организация
                department: null, // отдел
                description: null, // должность
            };
            this.checkbox = true;
            this.midelname = '';
            this.firstname = '';
            this.lastname ='';
            this.activeCompany = [];
            this.$store.dispatch("createContactModal/clearPhoneNumber",)
          },
          closeDialog () {
              this.clearForm();
              this.dialog = false;
              this.e1 = 1;
          },
          addAnotherContact() {
              this.clearForm();
              this.e1 = 1;
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
                            this.$store.dispatch("createContactModal/addPhoneNumber", response.data);
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
                            this.$store.dispatch("createContactModal/removePhoneNumber", mobilePhoneObj);
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
            },
            formatNumber(number) {
                return `+7(${number.toString().substring(1,4)})${number.toString().substring(4, 7)}-${number.toString().substring(7, 9)}-${number.toString().substring(9, 11)}`
            },
        }
    }
</script>

<style scoped>

</style>