
// Ubicación en el mapa al crear tienda
var map = L.map('map').setView([4.8087, -75.6906], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var marker;

map.on('click', function(e) {

    if (marker) {
        map.removeLayer(marker);
    }

    marker = L.marker(e.latlng).addTo(map);

    document.getElementById('latitud').value = e.latlng.lat;
    document.getElementById('longitud').value = e.latlng.lng;
});

// Dentro de tu archivo JS actual:
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. INTENTA LEER LAS COORDENADAS DE LOS INPUTS (Lo que viene de la BD)
    const inputLat = document.getElementById('id_latitud');
    const inputLng = document.getElementById('id_longitud');

    // Convertimos a número (float)
    let lat = parseFloat(inputLat.value);
    let lng = parseFloat(inputLng.value);

    // 2. VALIDACIÓN: ¿Hay coordenadas guardadas?
    if (!isNaN(lat) && !isNaN(lng)) {
        // Si existen (EDICIÓN), iniciamos el mapa en esa posición
        inicializarMapa(lat, lng);
    } else {
        // Si no existen (REGISTRO NUEVO), ponemos una por defecto (ej. Bogotá)
        inicializarMapa(4.6097, -74.0817);
    }
});

// Tu función de siempre, pero ahora recibe los parámetros
function inicializarMapa(lat, lng) {
    // Aquí va tu código de L.map('map').setView([lat, lng], 15)...
    // Y el marcador (L.marker) también debe usar esas variables [lat, lng]
}
