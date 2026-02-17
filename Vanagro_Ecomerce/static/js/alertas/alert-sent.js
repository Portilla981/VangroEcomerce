
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

      window.location.href = "{% url 'contactenos' %}";

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
