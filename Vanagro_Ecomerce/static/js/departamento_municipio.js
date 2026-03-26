
document.addEventListener("DOMContentLoaded", function () {
    const departamentoSelect = document.getElementById("departamento");
    const municipioSelect = document.getElementById("municipio");

    function cargarMunicipios() {
        let depId = departamentoSelect.value;
        if (!depId) {
            municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';
            return;
        }

        const idASeleccionar = municipioSelect.getAttribute("data-guardado") || municipioSelect.value;

        // LEER EL ID QUE ESTÁ GUARDADO EN LA BASE DE DATOS
        //let idGuardado = municipioSelect.getAttribute("data-guardado");

        fetch(`/ajax/Municipios/?departamento_id=${depId}`)
            .then(response => response.json())
            .then(data => {
                municipioSelect.innerHTML = '<option value="">Seleccione un municipio</option>';

                // Obtenemos el ID del atributo data-guardado
                let idGuardado = municipioSelect.getAttribute("data-guardado");
                
                data.forEach(m => {
                    let option = document.createElement("option");
                    option.value = m.id;
                    option.textContent = m.nombre_Municipio;

                     if (idASeleccionar && m.id == idASeleccionar) {
                        option.selected = true;
                    }
                    
                    // COMPROBACIÓN CLAVE: Si el ID coincide con el guardado, lo marcamos
                    // if (idGuardado && m.id == idGuardado) {
                    //     option.selected = true;
                    // }
                    
                    municipioSelect.appendChild(option);
                });
                // Limpiamos el atributo para que no interfiera en cambios manuales posteriores
                municipioSelect.setAttribute("data-guardado", "");
                // municipioSelect.removeAttribute("data-guardado");
            });
    }

    // Ejecutar al cambiar el departamento
    departamentoSelect.addEventListener("change", cargarMunicipios);

    // EJECUTAR AL CARGAR LA PÁGINA (Para que funcione al editar)
    if (departamentoSelect.value) {
        cargarMunicipios();
    }
});
