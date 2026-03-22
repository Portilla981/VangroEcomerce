// Carga en el dom y busca según el criterio organizado en la funcion.
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener("input", () => soloNumeros(input));
});

// Crea un evento para el campo de número de identificación, dependiendo del tipo de identificación seleccionado, se aplicará una función diferente para validar el formato del número de identificación, asegurando que solo se permitan números o una combinación de letras y números según corresponda.
document.addEventListener("DOMContentLoaded", () => {

    const tipo = document.getElementById("tipo_id");
    const numero = document.getElementById("number_id");

    console.log(tipo.value);    
    // numero.value = "";
    numero.addEventListener("input", function(e) {   

    if (tipo.value === "1") {
        // e.target.value = e.target.value.replace(/[^1-9]/g, '');
        soloNumeros(e);
    } 
    else if (tipo.value === "2" || tipo.value === "3") {
        // e.target.value = e.target.value.replace(/[^A-Za-z0-9]/g, '');
        letrasYNumeros(e);
    }   

    });


});


// Funcion para solo números 
function soloNumeros(e) {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
}

// Funcion de combinar números y letras 
function letrasYNumeros(e) {
    e.target.value = e.target.value.replace(/[^A-Za-z0-9]/g, '');
}


document.addEventListener("DOMContentLoaded", function() {
    const fechaInput = document.getElementById('fecha_nacimiento');
    const hoy = new Date();
    
    // --- LÍMITE SUPERIOR: MÁXIMO 18 AÑOS (MAYOR DE EDAD) ---
    const anioMax = hoy.getFullYear() - 18;
    
    // --- LÍMITE INFERIOR: MÁXIMO 90 AÑOS (AÑOS REALES) ---
    const anioMin = hoy.getFullYear() - 90;

    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const dia = String(hoy.getDate()).padStart(2, '0');

    // Formateamos ambas fechas para el input date (YYYY-MM-DD)
    const fechaMaxima = `${anioMax}-${mes}-${dia}`;
    const fechaMinima = `${anioMin}-${mes}-${dia}`;

    // Aplicamos ambas restricciones
    fechaInput.max = fechaMaxima; // No permite nacimientos después de esta fecha
    fechaInput.min = fechaMinima; // No permite nacimientos antes de esta fecha
    
    console.log(`Límites aplicados: Min ${fechaMinima} - Max ${fechaMaxima}`);
});
