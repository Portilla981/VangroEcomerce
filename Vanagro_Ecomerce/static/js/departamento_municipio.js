// document.getElementById("departamento").addEventListener("change", function () {
//         let depId = this.value;
//         fetch(`/ajax/Municipios/?departamento_id=${depId}`)
//             .then(response => response.json())
//             .then(data => {
//                 let municipioSelect = document.getElementById("municipio");
//                 municipioSelect.innerHTML = "";
//                 data.forEach(m => {
//                     let option = document.createElement("option");
//                     option.value = m.id;
//                     option.textContent = m.nombre_Municipio;
//                     municipioSelect.appendChild(option);
//                 });
//             });
//     });

// document.addEventListener("DOMContentLoaded", function () {
//     const departamentoSelect = document.getElementById("departamento");
//     const municipioSelect = document.getElementById("municipio");

//     // Función que hace la petición AJAX
//     function cargarMunicipios(depId, municipioSeleccionadoId = null) {
//         if (!depId) return; // Si no hay departamento, no hace nada

//         fetch(`/ajax/Municipios/?departamento_id=${depId}`)
//             .then(response => response.json())
//             .then(data => {
//                 municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
                
//                 data.forEach(m => {
//                     let option = document.createElement("option");
//                     option.value = m.id;
//                     option.textContent = m.nombre_Municipio;
                    
//                     // IMPORTANTE: Si estamos editando, marcamos el municipio que ya estaba guardado
//                     if (municipioSeleccionadoId && m.id == municipioSeleccionadoId) {
//                         option.selected = true;
//                     }
                    
//                     municipioSelect.appendChild(option);
//                 });
//             });
//     }

//     // EVENTO 1: Cuando el usuario cambia el departamento manualmente
//     departamentoSelect.addEventListener("change", function () {
//         cargarMunicipios(this.value);
//     });

//     // EVENTO 2: Al cargar la página (para edición)
//     // Obtenemos el ID del municipio que Django ya marcó como seleccionado en un input oculto o atributo data
//     const idMunicipioGuardado = "{{ form.instance.municipio.id }}"; 
//     cargarMunicipios(departamentoSelect.value, idMunicipioGuardado);
// });

document.addEventListener("DOMContentLoaded", function () {
    const departamentoSelect = document.getElementById("departamento");
    const municipioSelect = document.getElementById("municipio");

    function cargarMunicipios() {
        let depId = departamentoSelect.value;
        if (!depId) return;

        // LEER EL ID QUE ESTÁ GUARDADO EN LA BASE DE DATOS
        let idGuardado = municipioSelect.getAttribute("data-guardado");

        fetch(`/ajax/Municipios/?departamento_id=${depId}`)
            .then(response => response.json())
            .then(data => {
                municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
                
                data.forEach(m => {
                    let option = document.createElement("option");
                    option.value = m.id;
                    option.textContent = m.nombre_Municipio;

                    // COMPROBACIÓN CLAVE: Si el ID coincide con el guardado, lo marcamos
                    if (idGuardado && m.id == idGuardado) {
                        option.selected = true;
                    }
                    
                    municipioSelect.appendChild(option);
                });
            });
    }

    // Ejecutar al cambiar el departamento
    departamentoSelect.addEventListener("change", cargarMunicipios);

    // EJECUTAR AL CARGAR LA PÁGINA (Para que funcione al editar)
    if (departamentoSelect.value) {
        cargarMunicipios();
    }
});
