<template>

    <v-card
            class="mx-auto"
    >
        <v-sheet class="pa-4 primary lighten-2">
            <v-text-field
                    v-model="search"
                    label="Поиск по подразделениям"
                    dark
                    flat
                    solo-inverted
                    hide-details
                    clearable
                    clear-icon="mdi-close-circle-outline"
            ></v-text-field>
            <!--      <v-checkbox v-model="caseSensitive" dark hide-details label="Учитывать регистр"></v-checkbox>-->
        </v-sheet>
        <v-card-text>


            <!--    <v-card>-->
            <!--    <v-card-title>Фильтр по подразделениям</v-card-title>-->
            <v-treeview
                    :items="items"
                    dense
                    return-object
                    hoverable
                    multiple-active
                    :search="search"
                    :filter="filter"
                    :value="active"
                    open-on-click
                    item-text="company"
                    :selection-type="selectionType"
                    selectable
                    @input="exeCompanyFilter"
            >
                <template v-slot:label="{ item, open }">
                    <v-icon>
                        {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
                    </v-icon>
                </template>
                <template v-slot:label="{ item }">

                    {{ item.company === 'Employees' ? '***' : item.company }}

                </template>
            </v-treeview>
            <!--    </v-card>-->


        </v-card-text>
    </v-card>


</template>


<script>
    export default {
        name: "CompanyTree",
        props: {
           activeCompany: {
                type: Array
            },
            singleSelect: {
              type: Boolean
            },
            selectionType: {
              type: String
            },
        },
        data: () => ({
            items: [],
            active: [],
            search: null,
            caseSensitive: false,
        }),
        mounted() {
            this.getCompanyTree();
            // this.exeCompanyFilter();
            // this.$parent.$options.methods.changeSearchCompanyList([1,2,3,4]);
        },
        computed: {
            filter() {
                return this.caseSensitive
                    ? (item, search, textKey) => item[textKey].indexOf(search) > -1
                    : undefined
            },
        },
        watch: {
            'activeCompany': {
              handler: function (newVal, oldVal) {
                 console.log('CHANGED!!!');
                if (newVal != oldVal) {
                    console.log(this.active);
                    console.log('UPDATE ACTIVE DONT WORK');
                    this.active = newVal;
                    console.log(this.active);

                    // this.changeSelected();
                }
              }
            },
        },
        methods: {
            exeCompanyFilter(searchList) {
                console.log(searchList)
                this.$emit('search-company', searchList);
            },
            // changeSelected() {
            //     this.active = this.activeCompany;
            // },
            getCompanyTree() {
                // await
                this.$http.get(
                    `/contact/company/`, {
                        headers: {Authorization: `JWT ${localStorage.getItem('access')}`,},
                        params: {},

                    }
                )
                    .then(response => {
                        console.log(response)
                        this.items = response.data.results;

                    })
            }
        }
    }
</script>

<style scoped>

</style>