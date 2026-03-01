
let tiempoInactividad;
const TIEMPO_LIMITE = 300000; // 5 minutos en milisegundos

function resetTimer() {
    clearTimeout(tiempoInactividad);
    tiempoInactividad = setTimeout(cerrarSesion, TIEMPO_LIMITE);
}

function cerrarSesion() {
    window.location.href = "/Salir/";
}

// Detectar actividad
window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onclick = resetTimer;
document.onscroll = resetTimer;
