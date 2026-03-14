const mensajes = [
    "Cargando nueva interfaz...",
    "Optimizando recursos...",
    "Casi listo...",
    "Sincronizando datos..."
];

function cambiarInterfaz(callbackAccion) {
    const overlay = document.getElementById("loader-interfaz");
    const texto = document.getElementById("mensaje-carga");

    // 1. Mostrar mensaje aleatorio y activar overlay
    texto.textContent = mensajes[Math.floor(Math.random() * mensajes.length)];
    overlay.classList.add("active");

    // 2. Esperar un tiempo (ej. 2 segundos) para que el usuario vea el mensaje
    setTimeout(() => {
        
        // 3. Ejecutar el cambio de vista (tu lógica real)
        callbackAccion();

        // 4. Quitar el overlay
        setTimeout(() => {
            overlay.classList.remove("active");
        }, 500); // Pequeño margen para que cargue la nueva vista

    }, 2000); 
}

function navegarConMensaje(event) {
    // 1. Detenemos la navegación instantánea
    event.preventDefault();
    
    // Guardamos la URL a la que iba el usuario
    const urlDestino = event.currentTarget.href;

    // 2. Ejecutamos tu función de "Capa de carga" (la que creamos antes)
    cambiarInterfaz(() => {
        // 3. Cuando termine el mensaje, redirigimos manualmente
        window.location.href = urlDestino;
    });
}

// MODO DE USO:
// Cuando quieras cambiar de vista, llamas a la función:
// cambiarInterfaz(() => {
//    seccionHome.style.display = "none";
//    seccionPerfil.style.display = "block";
// });
