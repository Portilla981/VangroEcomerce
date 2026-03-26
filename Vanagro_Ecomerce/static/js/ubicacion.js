
// // Ubicación en el mapa al crear tienda
// var map = L.map('map').setView([4.8087, -75.6906], 13);

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// var marker;

// map.on('click', function(e) {

//     if (marker) {
//         map.removeLayer(marker);
//     }

//     marker = L.marker(e.latlng).addTo(map);

//     document.getElementById('latitud').value = e.latlng.lat;
//     document.getElementById('longitud').value = e.latlng.lng;
// });

// // Dentro de tu archivo JS actual:
// document.addEventListener('DOMContentLoaded', function() {
    
//     // 1. INTENTA LEER LAS COORDENADAS DE LOS INPUTS (Lo que viene de la BD)
//     const inputLat = document.getElementById('id_latitud');
//     const inputLng = document.getElementById('id_longitud');

//     // Convertimos a número (float)
//     let lat = parseFloat(inputLat.value);
//     let lng = parseFloat(inputLng.value);

//     // 2. VALIDACIÓN: ¿Hay coordenadas guardadas?
//     if (!isNaN(lat) && !isNaN(lng)) {
//         // Si existen (EDICIÓN), iniciamos el mapa en esa posición
//         inicializarMapa(lat, lng);
//     } else {
//         // Si no existen (REGISTRO NUEVO), ponemos una por defecto (ej. Bogotá)
//         inicializarMapa(4.6097, -74.0817);
//     }
// });

// // Tu función de siempre, pero ahora recibe los parámetros
// function inicializarMapa(lat, lng) {
//     // Aquí va tu código de L.map('map').setView([lat, lng], 15)...
//     // Y el marcador (L.marker) también debe usar esas variables [lat, lng]
// }


(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // 1. Referencias a elementos del DOM con IDs estándar de Django (ajusta si son diferentes)
        const mapContainer = document.getElementById('map');
        const inputLat = document.getElementById('id_latitud') || document.getElementById('latitud');
        const inputLng = document.getElementById('id_longitud') || document.getElementById('longitud');

        // Si no hay contenedor de mapa, salimos silenciosamente para evitar errores
        if (!mapContainer) return;

        // 2. Determinar coordenadas iniciales (Prioridad: Base de Datos > Bogotá)
        let latInicial = parseFloat(inputLat?.value) || 4.6097;
        let lngInicial = parseFloat(inputLng?.value) || -74.0817;
        let zoomInicial = (inputLat?.value) ? 16 : 13; // Más zoom si ya hay ubicación

        // 3. Inicializar el mapa
        const map = L.map('map').setView([latInicial, lngInicial], zoomInicial);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);

        // 4. Si ya existen coordenadas (EDICIÓN), colocar el marcador inicial
        let marker = null;
        if (inputLat?.value && inputLng?.value) {
            marker = L.marker([latInicial, lngInicial]).addTo(map);
        }

        // 5. Evento clic para actualizar o crear ubicación
        map.on('click', function(e) {
            const { lat, lng } = e.latlng;

            // Actualizar o crear el marcador
            if (marker) {
                marker.setLatLng(e.latlng);
            } else {
                marker = L.marker(e.latlng).addTo(map);
            }

            // Actualizar los inputs del formulario (si existen)
            if (inputLat) inputLat.value = lat.toFixed(6);
            if (inputLng) inputLng.value = lng.toFixed(6);
            
            console.log(`Ubicación seleccionada: ${lat}, ${lng}`);
        });

        // 6. Fix para mapas que cargan en pestañas o modales ocultos
        setTimeout(() => {
            map.invalidateSize();
        }, 500);
    });
})();
