// Obtener el elemento del mapa, para ser renderizado con los datos de latitud y longitud almacenados en la base de datos
var mapDiv = document.getElementById("map");

if (mapDiv) {
    // Si data-lat no existe, usamos una coordenada por defecto (ej. Bogotá: 4.60)
    var lat = parseFloat(mapDiv.dataset.lat) || 4.8087; 
    var lng = parseFloat(mapDiv.dataset.lng) || -75.6906;

    console.log("Latitud detectada:", lat);
    console.log("Longitud detectada:", lng);

    // Evitamos el error "Map container is already initialized"
    if (window.mapInstance) {
        window.mapInstance.remove();
    }

    // Guardamos la instancia en una variable global para poder limpiarla luego
    window.mapInstance = L.map('map').setView([lat, lng], 16);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(window.mapInstance);

    L.marker([lat, lng]).addTo(window.mapInstance);
    
    // Forzamos el redibujado por si acaso está en un modal
    setTimeout(() => { window.mapInstance.invalidateSize(); }, 200);
}


var myMap = null; // Variable global para controlar la instancia del mapa

function inicializarMapa(lat, lng) {
    // 1. Limpieza de seguridad para evitar el error "Map container is already initialized"
    var container = L.DomUtil.get('map');
    if (container != null) {
        container._leaflet_id = null; 
    }
    if (myMap !== null) {
        myMap.remove(); 
    }

    // 2. Crear el mapa centrado en la ubicación recibida
    myMap = L.map('map').setView([lat, lng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(myMap);

    // 3. Crear el marcador ARRASTRARLE (draggable: true)
    // Usamos las mismas coordenadas [lat, lng] que recibimos
    var marker = L.marker([lat, lng], {
        draggable: true
    }).addTo(myMap);

    // 4. EVENTO: Cuando el usuario termina de arrastrar el punto
    marker.on('dragend', function (event) {
        var position = marker.getLatLng();
        
        // Actualizamos los inputs de Django automáticamente
        document.getElementById('id_latitud').value = position.lat.toFixed(6);
        document.getElementById('id_longitud').value = position.lng.toFixed(6);
        
        // Centrar suavemente el mapa en la nueva posición
        myMap.panTo(new L.LatLng(position.lat, position.lng));
    });

    // 5. EVENTO OPCIONAL: Si el usuario hace clic en cualquier parte del mapa, el punto salta ahí
    myMap.on('click', function (e) {
        marker.setLatLng(e.latlng);
        document.getElementById('id_latitud').value = e.latlng.lat.toFixed(6);
        document.getElementById('id_longitud').value = e.latlng.lng.toFixed(6);
    });
}

// Asegúrate de que TODO lo que use 'id_latitud' esté envuelto en esto:
document.addEventListener('DOMContentLoaded', function() {
    const inputLat = document.getElementById('id_latitud');
    const inputLng = document.getElementById('id_longitud');

    // SOLO si los elementos existen en el HTML actual, ejecutamos el código
    if (inputLat && inputLng) {
        let lat = parseFloat(inputLat.value);
        let lng = parseFloat(inputLng.value);

        // Si no hay valores (NaN), ponemos unos por defecto
        if (isNaN(lat) || isNaN(lng)) {
            lat = 4.862163; 
            lng = -75.663444;
        }

        inicializarMapa(lat, lng);
    } 
    // Si no existen, el script no hace nada y no lanza el error "null"
});

