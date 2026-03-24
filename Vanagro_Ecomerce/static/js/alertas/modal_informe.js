function abrirModal() {
    document.getElementById("modalResumen").style.display = "block";
}

function cerrarModal() {
    document.getElementById("modalResumen").style.display = "none";
}

// Cerrar si el usuario hace clic fuera del recuadro blanco
window.onclick = function(event) {
    let modal = document.getElementById("modalResumen");
    if (event.target == modal) {
        cerrarModal();
    }
}