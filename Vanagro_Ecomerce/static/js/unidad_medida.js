// document.addEventListener("DOMContentLoaded", function () {

//     const tipo = document.getElementById("tipo_producto"); // frontend
//     const unidad = document.getElementById("id_unidad_medida"); // django

//     if (!tipo || !unidad) {
//         console.log("No se encontraron los elementos");
//         return;
//     }

//     // Guardar TODAS las opciones originales
//     const opcionesOriginales = Array.from(unidad.options);

//     //Reglas escalables
//     const reglas = {
//         liquido: ["Lt"],
//         solido: ["Kg", "Lb", "Und"],
//         otro: "ALL"
//     };

//     function filtrarUnidades() {
//         const valor = tipo.value;

//         // Limpiar opciones actuales
//         unidad.innerHTML = "";

//         let opcionesFiltradas;

//         if (reglas[valor] === "ALL") {
//             opcionesFiltradas = opcionesOriginales;
//         } else {
//             opcionesFiltradas = opcionesOriginales.filter(op =>
//                 reglas[valor].includes(op.value)
//             );
//         }

//         // Insertar nuevas opciones
//         opcionesFiltradas.forEach(op => {
//             unidad.appendChild(op.cloneNode(true));
//         });

//         // Evitar selección inválida
//         if (!opcionesFiltradas.some(op => op.value === unidad.value)) {
//             unidad.selectedIndex = 0;
//         }
//     }

//     // Evento al cambiar tipo
//     tipo.addEventListener("change", filtrarUnidades);

//     // Ejecutar al cargar (por si hay valor por defecto)
//     filtrarUnidades();

// });


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

});