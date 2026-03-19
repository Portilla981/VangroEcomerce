// 1. Definir variables globales para no perder la referencia
let mapaSeleccion = null;
let marcador = null;

function inicializarMapaSeleccion() {
    const mapDiv = document.getElementById("map");
    if (!mapDiv) return;

    // ELIMINAR MAPA PREVIO (Soluciona el error de la imagen)
    if (mapaSeleccion !== null) {
        mapaSeleccion.remove();
    }

    // Coordenadas iniciales (desde el dataset o por defecto)
    const latInicial = parseFloat(mapDiv.dataset.lat) || 4.6097;
    const lngInicial = parseFloat(mapDiv.dataset.lng) || -74.0817;

    // 2. CREAR EL MAPA
    mapaSeleccion = L.map('map').setView([latInicial, lngInicial], 16);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(mapaSeleccion);

    // 3. CREAR MARCADOR MOVIBLE (Draggable)
    marcador = L.marker([latInicial, lngInicial], {
        draggable: true  // ESTO permite que el usuario lo mueva
    }).addTo(mapaSeleccion);

    // 4. ACTUALIZAR INPUTS AL MOVER EL MARCADOR
    marcador.on('dragend', function(event) {
        const posicion = marcador.getLatLng();
        document.getElementById('lat_input').value = posicion.lat;
        document.getElementById('lng_input').value = posicion.lng;
        console.log("Nueva ubicación:", posicion.lat, posicion.lng);
    });

    // Opcional: Que el marcador salte a donde hagas clic en el mapa
    mapaSeleccion.on('click', function(e) {
        marcador.setLatLng(e.latlng);
        document.getElementById('lat_input').value = e.latlng.lat;
        document.getElementById('lng_input').value = e.latlng.lng;
    });
}

// Ejecutar al cargar la página
document.addEventListener("DOMContentLoaded", inicializarMapaSeleccion);
