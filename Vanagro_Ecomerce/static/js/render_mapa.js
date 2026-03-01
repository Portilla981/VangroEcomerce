// Obtener el elemento del mapa, para ser renderizado con los datos de latitud y longitud almacenados en la base de datos
var mapDiv = document.getElementById("map");
var lat = parseFloat(mapDiv.dataset.lat);
var lng = parseFloat(mapDiv.dataset.lng);

console.log("Latitud:", lat);
console.log("Longitud:", lng);

var map = L.map('map').setView([lat, lng], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([lat, lng]).addTo(map);