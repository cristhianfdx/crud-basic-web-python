<template>
    <div>
        <v-toolbar
                dark
                src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
            <v-toolbar-title>CRUD</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-app id="inspire">
            <v-card class="mt-10 mr-10 ml-10">
                <v-card-title>
                    <span>Empleados</span>
                    <v-spacer></v-spacer>
                    <v-text-field
                            v-model="search"
                            append-icon="mdi-magnify"
                            label="Buscar"
                            single-line
                            hide-details
                    ></v-text-field>
                </v-card-title>
                <v-data-table :headers="headers"
                              :items="employees"
                              sort-by="last_name"
                              class="elevation-2"
                              :calculate-widths="true"
                              :search="search"
                              locale="es-ES">
                    <template v-slot:top>
                        <v-toolbar flat color="white">
                            <v-spacer class="mx-4" inset vertical></v-spacer>
                            <v-dialog v-model="dialog" max-width="500px">
                                <template v-slot:activator="{ on }">
                                    <v-btn color="primary" dark class="mb-2" v-on="on">Nuevo Empleado</v-btn>
                                </template>
                                <v-card>
                                    <v-card-title>
                                        <span class="headline">{{ formTitle }}</span>
                                    </v-card-title>

                                    <v-card-text>
                                        <v-form
                                                ref="form"
                                                v-model="valid"
                                                :lazy-validation="true">
                                            <v-container>
                                                <v-col cols="11" class="mx-auto">
                                                    <v-text-field v-model="editedItem.first_name"
                                                                  required
                                                                  :counter="50"
                                                                  :rules="formRules.firstNameRules"
                                                                  label="Nombres">
                                                    </v-text-field>
                                                    <v-text-field v-model="editedItem.last_name"
                                                                  :counter="50"
                                                                  :rules="formRules.lastNameRules"
                                                                  label="Apellidos">
                                                    </v-text-field>
                                                    <v-text-field v-model="editedItem.document_number"
                                                                  label="Número de documento">
                                                    </v-text-field>
                                                    <v-menu
                                                            v-model="fromDateMenu"
                                                            :close-on-content-click="false"
                                                            :nudge-right="40"
                                                            transition="scale-transition"
                                                            offset-y
                                                            max-width="290px"
                                                            min-width="290px"
                                                    >
                                                        <template v-slot:activator="{ on }">
                                                            <v-text-field
                                                                    label="Fecha de nacimiento"
                                                                    prepend-icon="event"
                                                                    readonly
                                                                    :value="editedItem.birth_date"
                                                                    v-on="on"
                                                            ></v-text-field>
                                                        </template>
                                                        <v-date-picker
                                                                locale="es-ES"
                                                                v-model="editedItem.birth_date"
                                                                no-title
                                                                @input="fromDateMenu = false"
                                                                :min="minDate"
                                                                :max="maxDate"
                                                        ></v-date-picker>
                                                    </v-menu>
                                                    <v-text-field v-model="editedItem.mobile_number"
                                                                  label="Número telefónico"></v-text-field>
                                                    <v-combobox
                                                            v-model="editedItem.gender"
                                                            :items="genders"
                                                            label="Seleccione género"
                                                    ></v-combobox>
                                                </v-col>
                                            </v-container>
                                        </v-form>
                                    </v-card-text>

                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="red darken-1" text @click="close" type="button">Cancelar</v-btn>
                                        <v-btn color="green darken-1" text type="submit" :disabled="!valid">
                                            Guardar
                                        </v-btn>
                                    </v-card-actions>
                                </v-card>
                            </v-dialog>
                        </v-toolbar>
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <v-icon class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
                        <v-icon @click="deleteItem(item)" color="red lighten-1">mdi-delete</v-icon>
                    </template>
                    <template v-slot:no-data>
                        <span>No hay empleados registrados.</span>
                    </template>
                </v-data-table>
            </v-card>
        </v-app>
    </div>
</template>

<script>
    const URI = "/api/employee";
    import Swal from "sweetalert2";
    import axios from 'axios';

    export default {
        data: () => ({
            valid: true,
            search: '',
            fromDateMenu: false,
            fromDateVal: null,
            minDate: "1960-01-01",
            maxDate: `${new Date().getFullYear()}-${new Date().getMonth()}-${new Date().getDate()}`,
            dialog: false,
            genders: ['M', 'F', 'OTRO'],
            headers: [
                {text: "Apellidos", value: "last_name", align: "start"},
                {text: "Nombres", value: "first_name", sortable: false},
                {text: "Número de documento", value: "document_number", sortable: false},
                {text: "Fecha de nacimiento", value: "birth_date", sortable: false},
                {text: "Número telefónico", value: "mobile_number", sortable: false},
                {text: "Género", value: "gender", sortable: false},
                {text: "Acciones", value: "actions", sortable: false}
            ],
            employees: [],
            editedIndex: -1,
            editedItem: {
                first_name: "",
                last_name: "",
                document_number: "",
                birth_date: null,
                mobile_number: "",
                gender: ""
            },
            defaultItem: {
                first_name: "",
                last_name: "",
                document_number: "",
                birth_date: null,
                mobile_number: "",
                gender: ""
            },
            formRules: {
                firstNameRules: [
                    v => !!v || 'Nombres es requerido.',
                    v => (v && v.length <= 50) || 'Nombres no puede tener más de 50 carácteres',
                ],
                lastNameRules: [
                    v => !!v || 'Apellidos es requerido.',
                    v => (v && v.length <= 50) || 'Apellidos no puede tener más de 50 carácteres',
                ]
            }
        }),

        computed: {
            fromDateDisp() {
                return this.fromDateVal;
            },
            formTitle() {
                return this.editedIndex === -1 ? "Nuevo Empleado" : "Editar Empleado";
            }
        },

        watch: {
            dialog(val) {
                val || this.close();
            }
        },

        created() {
            this.initialize();
        },

        methods: {
            initialize() {
                this.getItems();
            },

            getItems() {
                axios.get(URI)
                    .then(response => {
                        this.employees = response.data;
                    });
            },

            editItem(item) {
                this.editedIndex = this.employees.indexOf(item);
                this.editedItem = Object.assign({}, item);
                this.dialog = true;
            },

            deleteItem(item) {
                const index = this.employees.indexOf(item);
                const {id} = item

                Swal.fire({
                    title: "¿Esta segur@?",
                    text: "¡No podrás revertir esto!",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "¡Si, borrar!"
                }).then(result => {
                    if (result.value) {
                        axios.delete(`${URI}/${id}`)
                            .then(response => {
                                if (response.status === 200 || response.status === 204) {
                                    this.employees.splice(index, 1);
                                    this.getItems();
                                    Swal.fire("¡Borrado!", "El empleado ha sido eliminado.", "success");
                                }
                            })
                            .catch(err => console.error(err));
                    }
                });
            },

            close() {
                this.dialog = false;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },

            save() {
                if (this.editedIndex > -1) {
                    const {id} = this.editedItem;
                    axios.put(`${URI}/${id}/`, this.editedItem)
                        .then(response => {
                            if (response.status === 201 || response.status === 200) {
                                this.getItems();
                            }
                        })
                        .catch(err => console.log(err));
                } else {
                    axios.post(`${URI}/`, this.editedItem)
                        .then(response => {
                            if (response.status === 201) {
                                this.employees.push(this.editedItem);
                                this.getItems();
                            }
                        })
                        .catch(err => console.log(err));
                }

                this.close();
            }
        }
    };
</script>

<style>
    * {
        font-family: "Roboto", "Lucida Grande", "DejaVu Sans", "Bitstream Vera Sans", Verdana, Arial, sans-serif;
    }

    #app {
        background: #f2fcfe;
    }
</style>