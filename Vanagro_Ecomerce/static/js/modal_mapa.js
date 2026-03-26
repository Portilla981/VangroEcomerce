
(function () {
    

// Usamos una variable global para el mapa del modal
let modalMapInstance = null;

const expandBtn = document.getElementById("expandMap");
const modal = document.getElementById("modalMapa");
const closeModalBtn = document.getElementById("closeModal");
const modalMapContainer = document.getElementById("modalMapContainer");

// 1. EXTRAER COORDENADAS (Importante: El div 'map' debe tener los data-attributes)
const mapaData = document.getElementById("map");

if (expandBtn && modal && mapaData) {
    
    expandBtn.addEventListener("click", () => {
        // Obtenemos lat/lng justo antes de abrir para asegurar que existen
        const lat = parseFloat(mapaData.dataset.lat) || 4.6097;
        const lng = parseFloat(mapaData.dataset.lng) || -74.0817;

        modal.style.display = "flex";

        // 2. EVITAR EL ERROR "Already Initialized"
        if (modalMapInstance) {
            modalMapInstance.remove(); // Borramos el mapa anterior antes de crear uno nuevo
        }

        // 3. INICIALIZAR MAPA EN EL MODAL
        modalMapInstance = L.map(modalMapContainer).setView([lat, lng], 16);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(modalMapInstance);

        L.marker([lat, lng]).addTo(modalMapInstance);

        // 4. SOLUCIÓN AL MAPA GRIS (Forzar renderizado)
        setTimeout(() => {
            modalMapInstance.invalidateSize();
        }, 300);
    });
}

// 5. CERRAR MODAL (Con validación para evitar el TypeError de addEventListener)
if (closeModalBtn) {
    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
        if (modalMapInstance) {
            modalMapInstance.remove();
            modalMapInstance = null;
        }
    });
}
})();
