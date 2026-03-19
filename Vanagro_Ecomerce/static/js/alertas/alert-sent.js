
let popupTimer;

function mostrarPopup(titulo, mensaje, tipo){

    const popup = document.getElementById("popup");
    const box = popup.querySelector(".popup-box");

    document.getElementById("popup-titulo").textContent = titulo;
    document.getElementById("popup-mensaje").textContent = mensaje;
    const icon = popup.querySelector(".popup__icon");

     box.classList.remove("popup-error","popup-ok","popup-warning","popup-info");

     icon.classList.remove(
        "fa-check",
        "fa-circle-xmark",
        "fa-triangle-exclamation",
        "fa-circle-info"
    );


    if(tipo === "error"){

        box.classList.add("popup-error");
        icon.classList.add("fa-circle-xmark");

    }else if(tipo === "warning"){

        box.classList.add("popup-warning");
        icon.classList.add("fa-triangle-exclamation");

    }else if(tipo === "info"){

        box.classList.add("popup-info");
        icon.classList.add("fa-circle-info");

    }else{

        box.classList.add("popup-ok");
        icon.classList.add("fa-check");

    }

    popup.style.display = "flex";

    clearTimeout(popupTimer);

    popupTimer = setTimeout(()=>{
        popup.style.display = "none";
    },2000);
}

function cerrarPopup(){
    document.getElementById("popup").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function(){

    const mensajes = document.querySelectorAll(".django-message");

    mensajes.forEach(msg => {

        const titulo = msg.dataset.titulo;
        const mensaje = msg.dataset.mensaje;
        const tipo = msg.dataset.tipo;

        mostrarPopup(titulo, mensaje, tipo);

    });

});