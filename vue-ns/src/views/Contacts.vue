<template>
    <v-container fluid>


        <v-row class="justify-center">

            <v-navigation-drawer
                    v-model="filterCompany"
                    absolute
                    temporary
                    width="700"
            >
                <CompanyTree
                        selectionType="independent"
                        :activeCompany="activeCompany"

                        @search-company="changeSearchCompanyList"
                ></CompanyTree>
            </v-navigation-drawer>
            <v-col
                    cols="12"
                    md="12"
            >
                <div v-if="!isAddressBook" class="text-center">
                    <v-btn class="ma-2" small rounded color="light-blue darken-3" dark
                           @click.prevent="changeIsAddressBook">
                        <v-icon left>mdi-book-open-variant</v-icon>
                        Выбрать из справочника
                    </v-btn>
                    <v-btn class="ma-2" small rounded color="teal darken-3" dark @click.prevent="toggleNewContactModal">
                        <v-icon left>mdi-pencil</v-icon>
                        Новый
                    </v-btn>
                    <v-btn class="ma-2" small rounded color="orange darken-3" dark @click.prevent="toggleCompanyFilter">
                        <v-icon left>mdi-filter</v-icon>
                        Фильтр
                    </v-btn>

                </div>


                <div v-else class="text-center">
                    <v-btn class="ma-2" small rounded color="light-blue darken-3" dark
                           @click.prevent="changeIsAddressBook">
                        <v-icon left>mdi-book-open-variant</v-icon>
                        Назад к моим контактам
                    </v-btn>
                    <v-btn class="ma-2" small rounded color="orange darken-3" dark @click.prevent="toggleCompanyFilter">
                        <v-icon left>mdi-filter</v-icon>
                        Фильтр
                    </v-btn>
                </div>


                <ContactList
                        @remove-company-filter="removeCompanyFilter"
                        :searchCompany="searchCompany"
                        :contactType="contactType"
                        :isAddressBook="isAddressBook"
                        mode="full"
                ></ContactList>
            </v-col>

        </v-row>


        <NewContactModal></NewContactModal>


    </v-container>
</template>

<script>
    import ContactList from "../components/Contacts/ContactList";
    import CompanyTree from "../components/Contacts/CompanyTree";
    import NewContactModal from "../components/Contacts/NewContactModal";


    export default {

        name: "Contacts",
        data: () => ({
            searchCompany: [],
            activeCompany: [],
            filterCompany: false,
            contactType: 'my-contacts',
            isAddressBook: false,
        }),
        props: {},
        components: {NewContactModal, ContactList, CompanyTree},
        methods: {
            changeSearchCompanyList(searchCompanyList) {
                this.searchCompany = searchCompanyList;
                console.log(this.searchCompany);
            },
            removeCompanyFilter(activeIDs) {
              this.activeCompany = activeIDs;
            },
            changeIsAddressBook() {
                this.isAddressBook = !this.isAddressBook;
                this.contactType = this.isAddressBook ? 'address-book' : 'my-contacts'
            },
            toggleCompanyFilter() {
                this.filterCompany = !this.filterCompany;
            },
            toggleNewContactModal() {
                this.$store.dispatch("createContactModal/openDialogCreateContact");
            }
        }
    }
</script>

<style scoped>

</style>