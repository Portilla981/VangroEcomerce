const botones = document.querySelectorAll(".user-list__action-btn--img")

const modal = document.getElementById("modalImagen")
const productoInput = document.getElementById("producto_id")
const preview = document.getElementById("previewImagen")

botones.forEach(btn => {

    btn.addEventListener("click", function(){

        // console.log("click detectado")

        let id = this.dataset.id
        let imagen = this.dataset.imagen

        productoInput.value = id
        preview.src = imagen

        modal.style.display = "flex"

    })

})

document.getElementById("cerrarModal").onclick = function(){
    modal.style.display = "none"
}