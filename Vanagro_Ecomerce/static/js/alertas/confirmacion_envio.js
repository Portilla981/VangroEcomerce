(function () {

  const form = document.getElementById("contactForm");
  const confirmPopup = document.getElementById("confirmPopup");
  const sendingPopup = document.getElementById("sendingPopup");
  const successPopup = document.getElementById("successPopup");
  const thanksPopup = document.getElementById("thanksPopup");

  let redirectUrl = null;

  // Ocultar todos
  function hideAll() {
    confirmPopup.style.display = "none";
    sendingPopup.style.display = "none";
    successPopup.style.display = "none";
    thanksPopup.style.display = "none";
  }

  // Capturar botón enviar
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".sent-alert");
    if (!btn) return;

    redirectUrl = btn.dataset.url;
    e.preventDefault();

    if (!form.reportValidity()) return;

    confirmPopup.style.display = "flex";
  });

  // Confirmar envío
  document.getElementById("btnConfirm").onclick = () => {
    hideAll();
    sendingPopup.style.display = "flex";

    // Simular envío (2s)
    setTimeout(() => {
      hideAll();
      successPopup.style.display = "flex";

      // Mensaje éxito
      setTimeout(() => {
        hideAll();
        thanksPopup.style.display = "flex";

        // Redirección
        setTimeout(() => {
          if (redirectUrl) window.location.href = redirectUrl;
        }, 4000);

      }, 2000);

    }, 2000);

    // Si quieres enviar realmente el form:
    form.submit();
  };

  // Cancelar
  document.getElementById("btnCancel").onclick = () => {
    hideAll();
  };

})();
