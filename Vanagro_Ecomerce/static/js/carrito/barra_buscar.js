const buscador = document.getElementById("buscador-productos");
const categoria = document.getElementById("filtro-categoria");
const contenedor = document.getElementById("productos-container");

let timeout = null;

function cargarProductos(){

    const query = buscador.value;
    const cat = categoria.value;

    fetch(`/buscar-productos/?q=${query}&categoria=${cat}`)

    .then(res => res.json())

    .then(data => {
        contenedor.innerHTML = data.html;
    });

}

buscador.addEventListener("keyup", function(){

    clearTimeout(timeout);

    timeout = setTimeout(cargarProductos, 300);

});

categoria.addEventListener("change", cargarProductos);