function validarNumeros(selector = ".solo-numeros") {

    const inputs = document.querySelectorAll(selector);

    inputs.forEach(input => {

        // Evitar letras
        input.addEventListener("keypress", (e) => {
            if (!/[0-9]/.test(e.key)) {
                e.preventDefault();
            }
        });

        // Validar en tiempo real
        input.addEventListener("input", () => {
            let value = parseInt(input.value);

            if (isNaN(value) || value < 1) {
                input.value = "";
            }
        });

        // Evitar pegar texto inválido
        input.addEventListener("paste", (e) => {
            let paste = (e.clipboardData || window.clipboardData).getData("text");

            if (!/^\d+$/.test(paste)) {
                e.preventDefault();
            }
        });

    });
}


document.addEventListener("DOMContentLoaded", function () {  

    const categoria = document.getElementById("id_categoria");
    const unidad = document.getElementById("id_unidad_medida");

    if (!categoria || !unidad) {
        console.warn("Faltan elementos");
        return;
    }

    // Guardar opciones originales
    const opcionesOriginales = Array.from(unidad.options);

    //Reglas por categoría (ESCALABLE)
    const reglas = {
        "Lácteos": ["Lt"],
        "Frutas": ["Kg", "Lb", "Und"],
        "Verduras": ["Kg", "Lb", "Und"],
        "Granos": ["Kg", "Lb"],
        "Otros": "ALL"
    };

    function filtrarUnidades() {
        const valor = categoria.value;

        unidad.innerHTML = "";

        let opcionesFiltradas;

        if (!reglas[valor] || reglas[valor] === "ALL") {
            opcionesFiltradas = opcionesOriginales;
        } else {
            opcionesFiltradas = opcionesOriginales.filter(op =>
                reglas[valor].includes(op.value)
            );
        }

        opcionesFiltradas.forEach(op => {
            unidad.appendChild(op.cloneNode(true));
        });

        // Evitar selección inválida
        if (!opcionesFiltradas.some(op => op.value === unidad.value)) {
            unidad.selectedIndex = 0;
        }
    }

    categoria.addEventListener("change", filtrarUnidades);

    // Ejecutar al cargar (modo edición)
    filtrarUnidades();

    validarNumeros(); 
});