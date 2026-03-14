const modal = document.getElementById("modalRecuperar")

document
    .getElementById("abrirRecuperar")
    .addEventListener("click", function(e){

        e.preventDefault()

modal.style.display="flex" })

document
    .getElementById("cerrarModal")
    .addEventListener("click", function(){

modal.style.display="none" })