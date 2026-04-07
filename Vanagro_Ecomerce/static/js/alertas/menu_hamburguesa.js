document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("menuToggle");
    const menu = document.getElementById("menuList");
    const overlay = document.getElementById("overlay");

    console.log("toggle:", toggle);
    console.log("menu:", menu);

    function toggleMenu() {
        console.log("CLICK MENU"); // para verificar

        toggle.classList.toggle("active");
        menu.classList.toggle("active");

        if (overlay) {
            overlay.classList.toggle("active");
        }
    }

    if (toggle && menu) {
        toggle.addEventListener("click", toggleMenu);
    }
});