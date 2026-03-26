const modal = document.getElementById("modalRecuperar");
const btnAbrir = document.getElementById("abrirRecuperar");
const btnCerrar = document.getElementById("cerrarModal");

// Solo agregar el evento si el botón de abrir existe en el HTML
if (btnAbrir && modal) {
    btnAbrir.addEventListener("click", function(e) {
        e.preventDefault();
        modal.style.display = "flex";
    });
}

// Solo agregar el evento si el botón de cerrar existe
if (btnCerrar && modal) {
    btnCerrar.addEventListener("click", function() {
        modal.style.display = "none";
    });
}
