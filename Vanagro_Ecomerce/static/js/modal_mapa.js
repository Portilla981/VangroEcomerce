// Este modal es la superposición del mapa para mostrar la ubicación al usuario, el mapa se amplia por el botón y la funcion remarcada
const expandBtn = document.getElementById("expandMap");
const modal = document.getElementById("modalMapa");
const closeModalBtn = document.getElementById("closeModal");
const modalMapContainer = document.getElementById("modalMapContainer");
const mapa = document.getElementById("map");    
    
expandBtn.addEventListener("click", () => {
    modal.style.display = "flex"; // Mostrar el modal    
    // Aquí puedes inicializar un nuevo mapa o reutilizar el existente
    var modalMap = L.map(modalMapContainer).setView([lat, lng], 16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(modalMap);
    L.marker([lat, lng]).addTo(modalMap);
});

closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none"; // Ocultar el modal       
    // Aquí puedes limpiar el mapa del modal si es necesario
    modalMap.remove();
});