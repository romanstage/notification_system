<template>
    <v-container fluid>
          <h1>Шаблоны</h1>
                <v-row >
                    <v-col cols="6">
                        <v-text-field
                            v-model="search"
                            label="Введите название шаблона"
                            class="ml-1"
                            outlined
                            align="center"

                            ></v-text-field>

                    </v-col>
                    <v-col cols="6" align="end">

<!--                        <v-btn style="float: right;" x-large class="button" justify="right"-->
<!--                        @click="addTextTemplateModalShowToggle"><v-icon-->
<!--                                  class="mr-2"-->
<!--                                  >-->
<!--                                  mdi-file-outline-->
<!--                        </v-icon>Новый шаблон</v-btn>-->

                      <v-btn class="ma-2" small rounded color="teal darken-3" dark
                             @click="addTextTemplateModalShowToggle"><v-icon
                                        class="mr-2"
                                      >
                                      mdi-account-multiple-plus
                            </v-icon>Новый шаблон </v-btn>
                    </v-col>
                </v-row>

                <v-row>
                    <v-col cols="6">
                      <h1>Cписок шаблонов</h1>
                          <v-card
                               v-for="textTemplate in filteredList"
                                :key="textTemplate.id"
                                class="mx-auto mb-2"
                                max-width="800"
                               @click="displayTemplateDetails(textTemplate)"

                          >
                            <v-card-title>{{textTemplate.title}}</v-card-title>

                            <v-card-text class="text--primary">
                              <p class="textwrapper limitedtext">{{limitedTextTemplateLength(textTemplate.body)}}</p>
                            </v-card-text>

                          </v-card>
                    </v-col>

                    <v-col cols="6" v-if="this.textTemplateToShow">


                      <h1>Подробнее о шаблоне</h1>

                      <v-card v-bind="this.textTemplateToShow"
                                class="mx-auto"
                                max-width="800"
                          >
                          <v-row>
                          <v-col align="start">
                              <h3 class="ma-3">{{textTemplateToShow.title}}</h3>
                          </v-col>
                          <v-col align="end" justify="right" >
                              <v-tooltip top>
                              <template v-slot:activator="{ on, attrs }">
                              <v-btn class="mx-1" fab dark x-small color="primary"
                              v-bind="attrs"
                              v-on="on"
                               @click="openAndLoadTemplateToEdit">
                              <v-icon x-small dark>mdi-pencil</v-icon>
                              </v-btn>
                              </template>
                              <span>Редактирование шаблона</span>
                              </v-tooltip>

                              <v-tooltip top>
                              <template v-slot:activator="{ on, attrs }">
                              <v-btn class="mx-1" fab dark x-small color="red"
                              v-bind="attrs"
                              v-on="on"
                              @click="openDeleteModal(textTemplateToShow)">

                              <v-icon small dark>mdi-delete</v-icon>
                              </v-btn>
                              </template>
                              <span>Удалить шаблон</span>
                              </v-tooltip>

                          </v-col>
                    </v-row>
                        <v-container justify="center" align="center" >
                          <p class="textwrapper">{{textTemplateToShow.body}}</p>
                        </v-container>



                      </v-card>


                    </v-col>
                      <v-col cols="6" v-if="!this.textTemplateToShow">
                        <v-container id="hint_div">
                          <h2 class="text--disabled">Выберите шаблон слева</h2>



                        </v-container>
                      </v-col>
                  </v-row>



<!--      Модал подтверждения уделения шаблона-->
      <genericModal v-bind:message="this.message"
          v-on:emitConfirm="textTemplateDelete"
        ></genericModal>
<!--  Модал добавления нового шаблона    -->

        <v-dialog v-model="addTextTemplateModalShow"  max-width="800">
                <v-card>
                    <v-container fluid >
                      <v-form
                          ref="form"
                          lazy-validation
                        >

                                    <v-text-field fluid
                                      v-model="newTextTemplateTitle"
                                      :counter="50"
                                      label="Название шаблона"
                                      required
                                    ></v-text-field>


                                  <v-textarea fluid
                                      v-model="newTextTemplateBody"
                                      :counter="720"
                                      label="Текст шаблона"
                                      required
                                    ></v-textarea>
<!--                          <v-container fluid>-->
<!--                            <v-textarea-->
<!--                              clearable-->
<!--                              clear-icon="Очистить"-->
<!--                              label="Текс шаблона"-->
<!--                            ></v-textarea>-->
<!--                          </v-container>-->
                          <v-row>

                                    <v-btn
                                      color="success"
                                      class="mr-4"
                                      @click = "addTextTemplate"
                                    >
                                      Сохранить
                                    </v-btn>
                                    <v-btn
                                      color="error"
                                      class="mr-4"
                                      @click = "addTextTemplateModalShow = false"

                                    >
                                      Отмена
                                    </v-btn>
                              </v-row>
                        </v-form>
                </v-container>
            </v-card>
        </v-dialog>

      <!--  Модал редактирования шаблона   -->

        <v-dialog v-model="editTextTemplateModalShow"  max-width="800">
                <v-card>
                    <v-container fluid >
                      <v-form
                          ref="form"
                          lazy-validation
                        >

                                    <v-text-field fluid
                                      v-model="editTextTemplateTitle"
                                      :counter="50"
                                      label="Название шаблона"
                                      required
                                    ></v-text-field>


                                  <v-textarea fluid
                                      v-model="editTextTemplateBody"
                                      :counter="720"
                                      label="Текст шаблона"
                                      required
                                    ></v-textarea>
<!--                          <v-container fluid>-->
<!--                            <v-textarea-->
<!--                              clearable-->
<!--                              clear-icon="Очистить"-->
<!--                              label="Текс шаблона"-->
<!--                            ></v-textarea>-->
<!--                          </v-container>-->
                          <v-row>

                                    <v-btn
                                      color="success"
                                      class="mr-4"
                                      @click="saveTempalateEdited"

                                    >
                                      Сохранить
                                    </v-btn>
                                    <v-btn
                                      color="error"
                                      class="mr-4"
                                      @click = editTextTemplateModalShowToggle()

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
import lodash from "lodash"
import Axios from "axios";

    export default {
        name: "TemplateList",
         data() {
            return {
            search:'',
            textTemplates:null,
            addTextTemplateModalShow:false,
            editTextTemplateModalShow:false,
            deleteGroupModalShow:false,
            newTextTemplateTitle:null,
            newTextTemplateBody:null,
            editTextTemplateTitle:null,
            editTextTemplateBody:null,
            // groupDeleteModalMessage:null,
            message:null,
            textTemplateToDelete:null,
            textTemplateToShow:null,
            }
        },
      components: {
          genericModal,
      },
        methods:{
            addTextTemplateModalShowToggle(){
                  this.addTextTemplateModalShow = !this.addTextTemplateModalShow

              },

            editTextTemplateModalShowToggle(){
                  this.editTextTemplateModalShow = !this.editTextTemplateModalShow

              },

            addTextTemplate(){
                    this.addTextTemplateModalShowToggle()
                      console.log('Front add template function fired')
                      console.log('tmp title', this.newTextTemplateTitle)
                      console.log('tmp body', this.newTextTemplateBody)
                      this.$http.post(`/contact/edit-text-template/`,
                          {title: this.newTextTemplateTitle, body:this.newTextTemplateBody},
                      )

                      .then((response) => {
                      console.log(response);
                          if (response.status === 200) {
                              this.addGroupModalShow = false;
                              this.getTextTemplates();
                              this.newTextTemplateTitle = null
                              this.newTextTemplateBody = null
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

            openDeleteModal (textTemplateObject) {
                   console.log('Generic GroupDeteleModal function fired ')
                    console.log(textTemplateObject)
                   let message = `Удалить шаблон  ${textTemplateObject.title}`
                   this.message = message
                   this.textTemplateToDelete = textTemplateObject
                   // this.groupDeleteModalMessage = message
                   this.$store.dispatch("genericModal/openGenericModal", this.message);
                  // this.$store.dispatch("contactDetailModal/openDialogDetail", contact);

            },
            textTemplateDelete(){
              let textTemplateObject = this.textTemplateToDelete
              console.log('template id to delete', this.textTemplateToDelete.id)
                // this.$http.delete(`/contact/edit-text-template/${this.textTemplateToDelete.id}/`,)
                this.$http.delete(`/contact/edit-text-template/${this.textTemplateToDelete.id}/`)
                .then((response) => {
                  console.log(response.status)
                    // Удаление шаблона из vue
                    if (response.status === 204) {
                        const idx = this.textTemplates.indexOf(this.textTemplateDelete())
                        this.textTemplates.splice(idx, 1)
                        console.log(response);
                        this.$store.dispatch("alerts/addAlert",
                            {'typeAlert': 'success', 'text': `Шаблн ${textTemplateObject.title} удален.`});
                        this.textTemplateToShow = null;
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
            openAndLoadTemplateToEdit(){
              let id = this.textTemplateToShow.id
              this.editTextTemplateModalShowToggle()
              // console.log('Opened modeal to Edit template with ID', id)

                this.$http(
                    `/contact/edit-text-template/${id}/`)
                    .then(response => {

                    console.log("Template to edit", response.data)
                    this.editTextTemplateTitle = response.data.title;
                    this.editTextTemplateBody = response.data.body;

                    })


            },
            saveTempalateEdited(){
              let id = this.textTemplateToShow.id
                // Тут сделать редактирование прямо на странице
                console.log('Edit group with ID', id)
                this.$http.patch(`/contact/edit-text-template/${id}/`,
                          {title: this.editTextTemplateTitle, body:this.editTextTemplateBody},
                      )
                    .then(response => {
                    this.getTextTemplates();
                    this.editTextTemplateTitle = null
                    this.editTextTemplateBody = null
                    this.editTextTemplateModalShowToggle()

                    })

            },
            displayTemplateDetails(template) {
              this.textTemplateToShow = template
              console.log('TextTemlateToShow', template)
              this.scrollToTop()
            },


            getTextTemplates() {
                   this.$http(
                        `/contact/text-template/`,
                    )
                        .then(response => {

                    console.log("textTemplates downloaded")
                    console.log(response.data.results)
                    this.textTemplates = response.data.results;

                })
             },
            limitedTextTemplateLength(textTemplateBody) {
              let displayTextTemplateBody = textTemplateBody
              if (displayTextTemplateBody.length > 50){
               displayTextTemplateBody = displayTextTemplateBody.substr(0,50) + '...';
              }
              return displayTextTemplateBody
            },
            scrollToTop() {
                  window.scrollTo(0,0);
             }
          },
         mounted () {
             this.getTextTemplates()
              // console.log(_.chunk(this.groups, 3));
              // console.log(_.chunk(this.groups, 3))
        },
         computed: {
            filteredList() {
                if (this.textTemplates != null){
                    return this.textTemplates.filter(textTemplate => {
                        return textTemplate.title.toLowerCase().includes(this.search.toLowerCase())
                    })
                }
            },

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


#hint_div {
  color: black;
  width: 400px;
  height: 260px;
  display: flex;
  justify-content: center;
  align-items: center;
}

#hint {
  background: #06c;
  flex: 0 0 120px;
}
.textwrapper
{
  margin:5px 0;
  padding:3px;
  white-space: pre-wrap;
}
.limitedtext {
   overflow: hidden;
   text-overflow: ellipsis;
   display: -webkit-box;
   -webkit-line-clamp: 2; /* number of lines to show */
   -webkit-box-orient: vertical;
}
</style>