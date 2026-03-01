
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
