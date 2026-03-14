document.getElementById("departamento").addEventListener("change", function () {
        let depId = this.value;
        fetch(`/ajax/Municipios/?departamento_id=${depId}`)
            .then(response => response.json())
            .then(data => {
                let municipioSelect = document.getElementById("municipio");
                municipioSelect.innerHTML = "";
                data.forEach(m => {
                    let option = document.createElement("option");
                    option.value = m.id;
                    option.textContent = m.nombre_Municipio;
                    municipioSelect.appendChild(option);
                });
            });
    });