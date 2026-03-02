// Carga en el dom y busca según el criterio organizado en la funcion.
document.querySelectorAll('input[type="tel"]').forEach(input => {
    input.addEventListener("input", () => soloNumeros(input));
});

// Crea un evento para el campo de número de identificación, dependiendo del tipo de identificación seleccionado, se aplicará una función diferente para validar el formato del número de identificación, asegurando que solo se permitan números o una combinación de letras y números según corresponda.
document.addEventListener("DOMContentLoaded", () => {

    const tipo = document.getElementById("tipo_id");
    const numero = document.getElementById("number_id");
    
    numero.value = "";
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