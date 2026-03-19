// Obtener el elemento del mapa, para ser renderizado con los datos de latitud y longitud almacenados en la base de datos
// var mapDiv = document.getElementById("map");
// var lat = parseFloat(mapDiv.dataset.lat);
// var lng = parseFloat(mapDiv.dataset.lng);

// console.log("Latitud:", lat);
// console.log("Longitud:", lng);

// var map = L.map('map').setView([lat, lng], 16);

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// L.marker([lat, lng]).addTo(map);

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
