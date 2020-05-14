<template>
  <v-app id="inspire">
    <v-data-table :headers="headers" :items="employes" sort-by="last_name" class="elevation-1">
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title>CRUD</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark class="mb-2" v-on="on">Nuevo Empleado</v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.first_name" label="Nombres"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.last_name" label="Apellidos"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.document_number" label="Número de documento"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
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
                          locale="en-in"
                          v-model="editedItem.birth_date"
                          no-title
                          @input="fromDateMenu = false"
                          :min="minDate"
                          :max="maxDate"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.mobile_number" label="Número telefónico"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field v-model="editedItem.gender" label="Género"></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="red darken-1" text @click="close">Cancelar</v-btn>
                <v-btn color="blue darken-1" text @click="save">Guardar</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
        <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize">Reset</v-btn>
      </template>
    </v-data-table>
  </v-app>
</template>

<script>
const URI = "/api/employee";
import Swal from "sweetalert2";
import axios from 'axios';

export default {
  data: () => ({
    fromDateMenu: false,
    fromDateVal: null,
    minDate: "1960-01-01",
    maxDate: `${new Date().getFullYear()}-${new Date().getMonth()}-${new Date().getDate()}`,
    dialog: false,
    headers: [
      {
        text: "Nombres",
        align: "start",
        sortable: false,
        value: "first_name"
      },
      { text: "Apellidos", value: "last_name" },
      { text: "Número de documento", value: "document_number" },
      { text: "Fecha de nacimiento", value: "birth_date" },
      { text: "Número telefónico", value: "mobile_number" },
      { text: "Género", value: "gender" },
      { text: "Acciones", value: "actions", sortable: false }
    ],
    employes: [],
    editedIndex: -1,
    editedItem: {
      first_name: "",
      last_name: "",
      birth_date: null,
      mobile_number: "",
      gender: ""
    },
    defaultItem: {
      first_name: "",
      last_name: "",
      birth_date: null,
      mobile_number: "",
      gender: ""
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
          this.employes = response.data;
        });
    },

    editItem(item) {
      this.editedIndex = this.employes.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.employes.indexOf(item);
      const { id } = item

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
            if (response.status === 200 || response.status === 204){
              this.employes.splice(index, 1);
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
        const { id } = this.editedItem;
        axios.put(`${URI}/${id}/`, this.editedItem)
        .then(response => {
          if (response.status === 201 || response.status === 200){
            this.getItems();
          }
        })
        .catch(err => console.log(err));
      } else {
        axios.post(`${URI}/`, this.editedItem)
        .then(response => {
          if (response.status === 201){
            this.employes.push(this.editedItem);
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