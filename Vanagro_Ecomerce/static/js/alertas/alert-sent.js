
function confirmarEnvio() {
    return confirm("¿Seguro que deseas enviar el mensaje?");
}

// message-edit-product.js
(function () {
  const POPUP_DURATION = 2000; // Duración del popup (4 segundos)

  function showPopup() {
    const popup = document.getElementById("popupMessage");
    if (!popup) return;

    // Mostrar popup
    popup.style.display = "block";

    // Reiniciar animación si es necesario
    popup.offsetWidth;

    // Ocultar popup después del tiempo definido
    clearTimeout(popup.__hideTimeout);
    popup.__hideTimeout = setTimeout(() => {
      popup.style.display = "none";
      // Redireccion a una página vacía para evitar resubmission
      window.location.href = URL.createObjectURL(new Blob([], { type: "text/html" }));

    }, POPUP_DURATION);
  }

  // Detectar clicks en el botón
  document.addEventListener("click", (event) => {
    const btn = event.target.closest(".sent-alert");
    if (!btn) return;

    const form = btn.closest("form");

    if (form) {
      const isValid = form.reportValidity();
      if (!isValid) return;

      event.preventDefault();
      showPopup();
      return;
    }

    event.preventDefault();
    showPopup();
  });

  // Ocultar popup al cargar
  document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popupMessage");
    if (popup) popup.style.display = "none";
  });
})();

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