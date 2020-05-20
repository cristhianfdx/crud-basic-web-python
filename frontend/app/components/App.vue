<template>
    <div>
        <v-toolbar
                dark
                src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
            <v-toolbar-title>CRUD</v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-app id="inspire">
            <div class="text-center">
                <v-snackbar v-model="snackbar" :vertical="true" color="success" top="top">
                    {{successMessage}}
                    <v-btn
                            dark
                            text
                            timeout="4000"
                            @click="snackbar = false">
                        Cerrar
                    </v-btn>
                </v-snackbar>
            </div>
            <v-card class="mt-10 ma-12">
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
                            <v-dialog v-model="dialog" max-width="500px" persistent>
                                <template v-slot:activator="{ on }">
                                    <v-btn color="primary" dark class="mb-2" v-on="on">
                                        Nuevo Empleado
                                    </v-btn>
                                </template>
                                <v-card>
                                    <v-card-title>
                                        <span class="headline">{{ formTitle }}</span>
                                    </v-card-title>

                                    <v-card-text>
                                        <v-container>
                                            <v-alert
                                                    prominent
                                                    type="error"
                                                    icon="warning"
                                                    transition="scale-transition"
                                                    dismissible
                                                    :value="alert">
                                                {{errorSummary}}
                                            </v-alert>
                                            <v-form
                                                    ref="form"
                                                    v-model="valid"
                                                    lazy-validation>
                                                <v-col cols="11" class="mx-auto">
                                                    <v-text-field
                                                            v-model="editedItem.first_name"
                                                            :counter="50"
                                                            :rules="formRules.firstNameRules"
                                                            label="Nombres*">
                                                    </v-text-field>
                                                    <v-text-field
                                                            v-model="editedItem.last_name"
                                                            :counter="50"
                                                            :rules="formRules.lastNameRules"
                                                            label="Apellidos*">
                                                    </v-text-field>
                                                    <v-text-field
                                                            v-model="editedItem.document_number"
                                                            :counter="14"
                                                            :rules="formRules.documentNumberRules"
                                                            label="Número de documento*">
                                                    </v-text-field>
                                                    <v-menu
                                                            v-model="fromDateMenu"
                                                            :close-on-content-click="false"
                                                            :nudge-right="40"
                                                            transition="scale-transition"
                                                            offset-y
                                                            max-width="290px"
                                                            min-width="290px">
                                                        <template v-slot:activator="{ on }">
                                                            <v-text-field
                                                                    label="Fecha de nacimiento*"
                                                                    prepend-inner-icon="event"
                                                                    :rules="formRules.birthDateRules"
                                                                    readonly
                                                                    :value="editedItem.birth_date"
                                                                    v-on="on"
                                                            ></v-text-field>
                                                        </template>
                                                        <v-date-picker
                                                                locale="es-ES"
                                                                v-model="editedItem.birth_date"
                                                                no-title
                                                                :reactive="true"
                                                                @input="fromDateMenu = false"
                                                                :min="minDate"
                                                                :max="maxDate"
                                                        ></v-date-picker>
                                                    </v-menu>
                                                    <v-text-field
                                                            v-model="editedItem.mobile_number"
                                                            prepend-inner-icon="phone"
                                                            :counter="10"
                                                            :rules="formRules.phoneNumberRules"
                                                            label="Número telefónico*">
                                                    </v-text-field>
                                                    <v-text-field
                                                            v-model="editedItem.email"
                                                            :rules="formRules.emailRules"
                                                            label="Correo electrónico*">
                                                    </v-text-field>
                                                    <v-combobox
                                                            v-model="editedItem.gender"
                                                            :items="genders"
                                                            :rules="formRules.genderRules"
                                                            label="Seleccione género*">
                                                    </v-combobox>
                                                    <v-select
                                                            v-model="editedItem.department"
                                                            :items="departments"
                                                            :rules="formRules.departmentRules"
                                                            label="Seleccione Departamento*">
                                                    </v-select>
                                                </v-col>
                                            </v-form>
                                        </v-container>
                                        <small>*Campos requeridos</small>
                                    </v-card-text>
                                    <v-card-actions>
                                        <v-spacer></v-spacer>
                                        <v-btn color="red darken-1" text @click="close">Cerrar</v-btn>
                                        <v-btn color="light-green darken-1" text @click="save" :disabled="!valid">
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
            <template>
                <v-row justify="center">
                    <v-dialog v-model="departmentDialog" persistent max-width="600px">
                        <template v-slot:activator="{ on }">
                            <v-btn color="indigo darken-3" dark v-on="on">Administar Departamentos</v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                                <span class="headline">Administaci&oacute;n de Departamentos</span>
                            </v-card-title>
                            <v-card-text>
                                <v-container>
                                    <v-alert
                                            prominent
                                            type="error"
                                            icon="warning"
                                            transition="scale-transition"
                                            dismissible
                                            :value="depAlert">
                                        {{errorSummary}}
                                    </v-alert>
                                    <v-autocomplete
                                            v-model="selectedDepartments"
                                            :disabled="isDeleting"
                                            :items="items"
                                            filled
                                            chips
                                            color="blue-grey lighten-2"
                                            label="Seleccionar departamentos"
                                            item-text="name"
                                            item-value="name"
                                            multiple>
                                        <template v-slot:selection="data">
                                            <v-chip
                                                    v-bind="data.attrs"
                                                    :input-value="data.selected"
                                                    close
                                                    @click="data.select"
                                                    @click:close="remove(data.item)">
                                                {{ data.item.name }}
                                            </v-chip>
                                        </template>
                                        <template v-slot:item="data">
                                            <template v-if="typeof data.item !== 'object'">
                                                <v-list-item-content v-text="data.item"></v-list-item-content>
                                            </template>
                                            <template v-else>
                                                <v-list-item-content>
                                                    <v-list-item-title v-html="data.item.name"></v-list-item-title>
                                                </v-list-item-content>
                                            </template>
                                        </template>
                                        <template v-slot:no-data>
                                            <span>No hay departamentos registrados.</span>
                                        </template>
                                    </v-autocomplete>
                                    <v-card-subtitle class="text-center mt-3">
                                        <span class="headline">Crear Departamento</span>
                                    </v-card-subtitle>
                                    <v-form
                                            ref="formDep"
                                            lazy-validation
                                            v-model="frmValid">
                                        <v-row>
                                            <v-col cols="8" class="mx-auto">
                                                <v-text-field
                                                        label="Nombre*"
                                                        v-model="departmentName"
                                                        :rules="formRules.departmentNameRules"
                                                        required>
                                                </v-text-field>
                                                <small>*Campo requerido</small>
                                            </v-col>
                                        </v-row>
                                    </v-form>
                                </v-container>
                            </v-card-text>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="orange darken-4" text @click="departmentDialog = false">Cerrar</v-btn>
                                <v-btn color="red darken-4" text @click="deleteDepartments">Borrar</v-btn>
                                <v-btn color="green darken-1" text @click="saveDepartment">Crear</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-row>
            </template>
            <template>
                <v-footer absolute class="font-weight-medium" height="80px">
                    <v-spacer></v-spacer>
                    <div>By: Cristhian Forero &copy; {{ new Date().getFullYear() }}</div>
                </v-footer>
            </template>
        </v-app>
    </div>
</template>

<script>
    import Swal from "sweetalert2";
    import $axios from 'axios';
    import moment from 'moment';

    const EMPLOYEE_URI = "/api/employee";
    const DEPARTMENT_URI = "/api/department";

    const DATE_FORMAT = "YYYY-MM-DD";

    export default {
        data: () => ({
            isDeleting: false,
            departmentName: '',
            loading: false,
            valid: true,
            frmValid: true,
            alert: false,
            depAlert: false,
            snackbar: false,
            search: '',
            selectedDepartments: [],
            select: null,
            items: [],
            fromDateMenu: false,
            fromDateVal: null,
            minDate: moment().subtract(50, 'y').format(DATE_FORMAT),
            maxDate: moment().format(DATE_FORMAT),
            dialog: false,
            departmentDialog: false,
            genders: ['M', 'F', 'OTRO'],
            headers: [
                {text: "Apellidos", value: "last_name", align: "start"},
                {text: "Nombres", value: "first_name", sortable: false},
                {text: "Número de documento", value: "document_number", sortable: false},
                {text: "Fecha de nacimiento", value: "birth_date", sortable: false},
                {text: "Número telefónico", value: "mobile_number", sortable: false},
                {text: "Email", value: "email", sortable: false},
                {text: "Departamento", value: "department", sortable: false},
                {text: "Género", value: "gender", sortable: false},
                {text: "Acciones", value: "actions", sortable: false}
            ],
            employees: [],
            editedIndex: -1,
            editedItem: {
                first_name: "",
                last_name: "",
                document_number: "",
                birth_date: "",
                mobile_number: "",
                email: "",
                gender: "",
                department: null
            },
            defaultItem: {
                first_name: "",
                last_name: "",
                document_number: "",
                birth_date: "",
                mobile_number: "",
                email: "",
                gender: "",
                department: null,
            },
            errorMessage: "",
            successMessage: "",
            departments: [],
            departmentId: null,
            formRules: {
                firstNameRules: [
                    v => !!v || 'Los Nombres son obligatorios.',
                    v => (v && v.length <= 50) || 'Los Nombres no pueden tener más de 50 carácteres.',
                    v => /^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/.test(v) || 'No puede contener carácteres especiales ni números'
                ],
                lastNameRules: [
                    v => !!v || 'Los Apellidos son obligatorios.',
                    v => (v && v.length <= 50) || 'Los Apellidos no pueden tener más de 50 carácteres.',
                    v => /^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$/.test(v) || 'No puede contener carácteres especiales ni números'
                ],
                documentNumberRules: [
                    v => !!v || 'El Número de documento es obligatorio.',
                    v => (v && v.length <= 14) || 'El Número de documento no puede tener más de 14 carácteres.',
                    v => /^[a-zA-Z0-9]*$/.test(v) || 'Solo puede contener carácteres alfanúmericos y sin espacios.'
                ],
                phoneNumberRules: [
                    v => !!v || 'El Número telefónico es obligatorio',
                    v => (v && v.length >= 7 && v.length <= 10) || 'El Número telefónico  debe tener entre 7 y 10 dígitos.',
                    v => /\d$/.test(v) || 'Solo se permiten números.'
                ],
                birthDateRules: [
                    v => !!v || 'La fecha de nacimiento es obligatoria',
                    v => moment().diff(moment(v), 'years') >= 18 || 'El Empleado debe ser mayor de edad (18 años)',
                ],
                emailRules: [
                    v => !!v || 'El correo electrónico es obligatorio.',
                    v => /.+@.+\..+/.test(v) || 'Debe ingresar un correo electrónico válido.',
                ],
                genderRules: [v => !!v || 'El Género es obligatorio'],
                departmentRules: [v => !!v || 'El Departamento es obligatorio'],
                departmentNameRules: [
                    v => !!v || 'El Nombre es obligatorio',
                    v => /^[a-zA-Z0-9]*$/.test(v) || 'Solo puede contener carácteres alfanúmericos y sin espacios.'
                ]
            }
        }),

        computed: {
            fromDateDisplay() {
                return this.fromDateVal;
            },
            formTitle() {
                return this.editedIndex === -1 ? "Nuevo Empleado" : "Editar Empleado";
            },
            errorSummary() {
                return this.errorMessage;
            }
        },

        watch: {
            dialog(val) {
                val || this.close();
            },
            departmentDialog(val) {
                val || this.closeFormDep();
            }
        },

        created() {
            this.initialize();
        },

        methods: {
            initialize() {
                this.getDepartments();
                this.getItems();
            },

            getItems() {
                $axios.get(EMPLOYEE_URI)
                    .then(response => {
                        this.employees = response.data.map(value => {
                            value.department = value.department.name;
                            return value;
                        });
                    })
                    .catch(e => this.showErrorAlert(e))
            },

            editItem(item) {
                this.editedIndex = this.employees.indexOf(item);
                let edited = this.employees[this.editedIndex];
                item.department = this.departments.filter(val => val.text === edited.department)[0].value;
                this.getItems();
                this.editedItem = Object.assign({}, item);
                this.dialog = true;
            },

            deleteItem(item) {
                const index = this.employees.indexOf(item);
                const {id} = item;
                this.showSweetAlert("employee", index, id);
            },

            removeEmployee(params) {
                $axios.delete(`${EMPLOYEE_URI}/${params[1]}/`)
                    .then(response => {
                        if (response.status === 200) {
                            this.employees.splice(params[0], 1);
                            this.getItems();
                            this.showSuccessAlert(response);
                        }
                    })
                    .catch(e => this.showErrorAlert(e));
            },

            getDepartments() {
                $axios.get(DEPARTMENT_URI)
                    .then(response => {
                        const {data} = response;
                        this.departments = data.map(val => {
                            return {text: val.name, value: val.id}
                        });

                        this.items = data.map(val => {
                            return {name: val.name}
                        });
                    })
                    .catch(e => this.showErrorAlert(e))
            },

            close() {
                this.dialog = false;
                this.$refs.form.reset();
                this.$refs.form.resetValidation();
                this.valid = false;
                this.$nextTick(() => {
                    this.editedItem = Object.assign({}, this.defaultItem);
                    this.editedIndex = -1;
                });
            },

            save() {
                if (this.isValidForm()) {
                    if (this.editedIndex > -1) {
                        const {id} = this.editedItem;
                        $axios.put(`${EMPLOYEE_URI}/${id}/`, this.editedItem)
                            .then(response => {
                                if (response.status === 200) {
                                    this.getItems();
                                    this.close();
                                    this.showSuccessAlert(response);
                                }
                            })
                            .catch(err => console.log(err));
                    } else {
                        $axios.post(`${EMPLOYEE_URI}/`, this.editedItem)
                            .then(response => {
                                if (response.status === 201) {
                                    this.employees.push(this.editedItem);
                                    this.getItems();
                                    this.close();
                                    this.showSuccessAlert(response);
                                }
                            })
                            .catch(e => this.showErrorAlert(e));
                    }
                }
            },

            saveDepartment() {
                if (this.$refs.formDep.validate()) {
                    $axios.post(`${DEPARTMENT_URI}/`, {
                        name: this.departmentName.toUpperCase()
                    })
                        .then(response => {
                            if (response.status === 201) {
                                this.getDepartments();
                                this.closeFormDep();
                                this.showSuccessAlert(response);
                            }
                        })
                        .catch(e => this.showErrorAlert(e));
                }
            },

            deleteDepartments() {
                if (this.selectedDepartments.length === 0) {
                    this.depAlert = true;
                    this.errorMessage = "Se debe seleccionar por lo menos un departamento para poder borrar.";
                    this.hideErrorAlert();
                } else {
                    this.showSweetAlert("");
                }
            },

            removeDepartments() {
                const departmentsToDelete = this.departments.map(value => {
                    const temp = this.selectedDepartments.filter(sel => sel === value.text);
                    const name = temp[0];
                    if (name) return {id: value.value, name};
                });

                departmentsToDelete.forEach(dep => {
                    if (dep) {
                        const {id} = dep;
                        $axios.delete(`${DEPARTMENT_URI}/${id}/`)
                            .then(response => {
                                if (response.status === 200) {
                                    this.getDepartments();
                                    this.closeFormDep();
                                    this.showSuccessAlert(response);
                                }
                            })
                            .catch(e => this.showErrorAlert(e));
                    }
                });
            },

            isValidForm() {
                return this.$refs.form.validate();
            },

            closeFormDep() {
                this.$refs.formDep.reset();
                this.$refs.formDep.resetValidation();
                this.selectedDepartments = [];
                this.departmentDialog = false;
            },

            showErrorAlert(e) {
                const {error} = e.response.data;
                if (this.dialog) {
                    this.alert = true;
                }

                if (this.departmentDialog) {
                    this.depAlert = true;
                }

                this.errorMessage = error;
                this.hideErrorAlert();
            },

            showSuccessAlert(response) {
                const {msg} = response.data;
                this.snackbar = true;
                this.successMessage = msg;
                this.hideSuccessAlert()
            },

            hideErrorAlert() {
                setTimeout(() => {
                    if (this.dialog) {
                        this.alert = false;
                    }

                    if (this.departmentDialog) {
                        this.depAlert = false;
                    }
                    this.errorMessage = "";
                }, 3000);
            },

            hideSuccessAlert() {
                setTimeout(() => {
                    this.snackbar = false;
                    this.successMessage = "";
                }, 3500);
            },

            showSweetAlert(action, ...args) {
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
                        if (action === 'employee') {
                            this.removeEmployee(args);
                        } else {
                            this.removeDepartments();
                        }
                    }
                });
            },

            remove(item) {
                const index = this.selectedDepartments.indexOf(item.name);
                if (index >= 0) this.selectedDepartments.splice(index, 1)
            },
        },
    }

</script>

<style>
    * {
        font-family: "Roboto", "Lucida Grande", "DejaVu Sans", "Bitstream Vera Sans", Verdana, Arial, sans-serif;
    }

    #app {
        background: #f2fcfe;
    }
</style>