
let popupTimer; 

function mostrarPopup(titulo, mensaje, tipo, esConfirmacion = false, autoCerrar = null) {

    const popup = document.getElementById("popup");
    const box = popup.querySelector(".popup-box");
    const icon = popup.querySelector(".popup__icon");
    const btnCerrar = popup.querySelector(".btn-popup-cerrar");
    const btnConfirmar = document.getElementById("btn-confirmar-accion");
    const mensaje_popup = popup.querySelector(".popup__time");

    // Reset inicial
    if (btnConfirmar) btnConfirmar.style.display = "none";

    if (btnCerrar) {
        btnCerrar.style.display = "none";
        btnCerrar.textContent = "Entendido";
    }

    if (mensaje_popup) mensaje_popup.style.display = "none";

    document.getElementById("popup-titulo").textContent = titulo;
    document.getElementById("popup-mensaje").textContent = mensaje;

    // Estilos
    box.classList.remove("popup-error", "popup-ok", "popup-warning", "popup-info");
    icon.classList.remove("fa-check", "fa-circle-xmark", "fa-triangle-exclamation", "fa-circle-info");

    if (tipo === "error") {

        box.classList.add("popup-error");
        icon.classList.add("fa-circle-xmark");

        if (btnCerrar){
            btnCerrar.style.display = "inline-block";
            btnCerrar.textContent = "Entendido";
        }

    } else if (esConfirmacion) {

        box.classList.add("popup-warning");
        icon.classList.add("fa-triangle-exclamation");

        if (btnConfirmar) btnConfirmar.style.display = "inline-block";

        if (btnCerrar) {
            btnCerrar.style.display = "inline-block";
            btnCerrar.textContent = "No, volver";
        }

    } else {

        box.classList.add(tipo === "ok" ? "popup-ok" : "popup-info");
        icon.classList.add(tipo === "ok" ? "fa-check" : "fa-circle-info");

        if (mensaje_popup) mensaje_popup.style.display = "inline-block";
    }

    popup.style.display = "flex";

    // Timer
    clearTimeout(popupTimer);

    let tiempo = null;

    if (!esConfirmacion) {
        if (tipo === "error") {
            tiempo = autoCerrar ? 2400 : null;
        } else {
            tiempo = 2400;
        }
    }

    if (tiempo) {
        popupTimer = setTimeout(cerrarPopup, tiempo);
    }
}


function confirmarAccion(titulo, mensaje, tipo, callback) {

    mostrarPopup(titulo, mensaje, tipo, true);

    clearTimeout(popupTimer);

    const btnConfirmar = document.getElementById("btn-confirmar-accion");

    if (btnConfirmar) {

        btnConfirmar.style.display = "inline-block";

        //Limpieza antes de asignar
        btnConfirmar.onclick = null;

        btnConfirmar.onclick = function() {
            callback();
            cerrarPopup();
        };
    }
}


function cerrarPopup(){

    const popup = document.getElementById("popup");
    const btnConfirmar = document.getElementById("btn-confirmar-accion");
    const btnCerrar = popup.querySelector(".btn-popup-cerrar");
    const mensaje_popup = popup.querySelector(".popup__time");

    popup.style.display = "none";
    
    if (btnConfirmar) {
        btnConfirmar.style.display = "none";
        btnConfirmar.onclick = null;
    }

    if (btnCerrar) {
        btnCerrar.textContent = "Entendido";
    }

    if (mensaje_popup) {
        mensaje_popup.style.display = "none";
    }
}


document.addEventListener("DOMContentLoaded", function(){

    //1. Django messages
    const mensajes = document.querySelectorAll(".django-message");
    // const auto = msg.dataset.auto === "true";

    mensajes.forEach(msg => {
        mostrarPopup(
            msg.dataset.titulo,
            msg.dataset.mensaje,
            msg.dataset.tipo,
            // false,
            // true
        );
    });

    //2. Botones de confirmación
    document.querySelectorAll(".btn-confirmar").forEach(boton => {


        boton.addEventListener("click", function(e){
            e.preventDefault(); 
            
            const boton = this;
            const formId = this.dataset.form;
            const titulo = this.dataset.titulo;
            const mensaje = this.dataset.mensaje;
            const url = this.dataset.url;
            console.log("Formulario:", formId);
            console.log(document.getElementById(formId));

            if (formId) {
                const formulario = document.getElementById(formId);

                if (formulario && !formulario.checkValidity()) {
                    formulario.reportValidity();
                    return;
                }
            }

            

            confirmarAccion(titulo, mensaje, "warning", () => {
                if (url) {
                    window.location.href = url;
                } else if (formId) {
                    // document.getElementById(formId).submit();
                    const formulario = document.getElementById(formId);
                    formulario.requestSubmit(boton);
                }
            });

        });

    });

    // 3. Botón cerrar popup
    const btnCerrar = document.querySelector(".btn-popup-cerrar");

    if (btnCerrar) {
        btnCerrar.addEventListener("click", cerrarPopup);
    }

});