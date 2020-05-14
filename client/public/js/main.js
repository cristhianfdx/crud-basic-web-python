const formComponent = {
    template: `
        <div class="card m-5">
            <div class="card-header">
            </div>
            <div class="card-body"></div>
        </div>

    `
}

const tableComponent = {
    template: `
        <table class="table m-5">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">Nombre</th>
                    <th scope="col">Número documento</th>
                    <th scope="col">Número teléfonico</th>
                    <th scope="col">Fecha de nacimiento</th>
                    <th scope="col">Avatar</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

    `
}


new Vue({
    el: '#app',
    components: {
        'form-component' : formComponent,
        'table-component' : tableComponent
    }
});