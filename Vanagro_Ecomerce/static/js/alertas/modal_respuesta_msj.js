const botones = document.querySelectorAll(".btn-abrir-modal")
const modal = document.getElementById("modalRespuesta")

const asuntoSpan = document.getElementById("modal-asunto")
const mensajeSpan = document.getElementById("modal-mensaje")
const mensajeIdInput = document.getElementById("mensaje-id")



botones.forEach(btn => {
    btn.addEventListener("click", function(){
        
        document.querySelector("textarea[name='respuesta']").value = ""

        //Obtener datos del botón
        const id = this.dataset.id
        const asunto = this.dataset.asunto
        const mensaje = this.dataset.mensaje

        //Insertarlos en el modal
        asuntoSpan.textContent = asunto
        mensajeSpan.textContent = mensaje
        mensajeIdInput.value = id

        //Mostrar modal
        modal.style.display = "flex"
    })
})

document.getElementById("cerrarModal").onclick = function(){
    modal.style.display = "none"
}