<template>
<v-row align="start" justify="center">
<!--    <v-col class="col-6">-->
<v-form>
    <v-text-field
  v-model="newMobile"
  :rules="phoneRules"
    prepend-inner-icon="+7"
  label="Введите номер"

   placeholder="(999)123-45-67"
    >
<!--        <dev slot="prepend">+7</dev>-->
    </v-text-field>

    <v-btn
      color="success"
      class="mr-4"
      v-on:click="sendNewMobile"
      x-small
    >Добавить
    </v-btn>

    <v-btn
      color="error"
      class="mr-4"
      @click="closeMobileForm"
      x-small
    > Отмена
    </v-btn>
  </v-form>
<!--</v-col>-->
</v-row>


</template>

<script>


  export default {
      data() {
          return {
              phoneRules: [
                v => !!v || 'Номер не введен',
                v => v.replace(/[^\d]/g, '').length == 10 || 'Номер должен содиржать 10 цифр',
                v => v.replace(/[^\d]/g, '').substring(0,1) != '7' || 'Номер не должен начинаться на 7',
                v => v.replace(/[^\d]/g, '').substring(0,1) != '8' || 'Номер не должен начинаться на 8',

              ],
              newMobile: '',

            }
      },
      watch: {
          newMobile (newVal, oldVal) {
          //
                  console.log('change number');
                  console.log(newVal.replace(/[^\d]/g, ''))
                  if (newVal.replace(/[\d]/g, '').length <= 11) {
                      let number = newVal.replace(/[^\d]/g, '');
                      console.log(number)

                      // if (number.substring(0,1) != '7' || number.substring(0,1) != '8') {console.log(number.substring(0,1))}
                      this.newMobile = `(${number.substring(0,3)})${number.substring(3, 6)}-${number.substring(6, 8)}-${number.substring(8, 10)}`
                      // return newVal.replace(/[^\d]/g, '')
                      console.log(this.newMobile)
                  }
          //
          }

    },
      components: {

      },
          methods: {

              sendNewMobile() {
                  let modifiedPhone = `7${this.newMobile.replace(/[^\d]/g, '')}`;
                  let checkNumber = this.newMobile.replace(/[^\d]/g, '')
                  console.log(checkNumber.length)
                  if (checkNumber.length != 10) {
                    console.log('телефон указан не полностью')
                    this.$store.dispatch("alerts/addAlert", {
                        typeAlert:'orange',
                        text:'Неверный номер'
                            },
                  );
                    return;



                  }

                  else if (checkNumber.substring(0,1) == '7' || checkNumber.substring(0,1) == '8') {
                      this.$store.dispatch("alerts/addAlert", {
                        typeAlert:'orange',
                        text:`Код оператора не должен начинаться с ${checkNumber.substring(0,1)}`
                            },
                    );
                      return;
                  }
                  else {
                      this.$emit('emitNewMobilePhone', modifiedPhone);
                      return;
                  }

              },
              closeMobileForm() {
                  this.$emit('closeMobileForm')

              }
          }
        }
</script>