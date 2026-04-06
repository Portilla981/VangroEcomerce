/* carga del html */
document.addEventListener("DOMContentLoaded", function(){
    /* evento de escucha-> clic */
    document.addEventListener("click", function(e){

        /* busca donde fue el evento (busca la fila) */
        const fila = e.target.closest("tr");
        /* si no encuentra la fila no hace nada */
        if (!fila) return;

        /* obtiene el id del producto */
        const itemId = fila.dataset.id;
        /* busca el campo donde esta la cantidad */
        const input = fila.querySelector(".cantidad-input");
        /* busca el campo donde esta el subtotal */
        // const subtotalCell = fila.querySelector(".subtotal");
        /* busca el campo del total del carrito */
        // const totalGeneral = document.querySelector(".total-general");

        /* cuando se da clic en sumar. verifica la cantidad actual, que no supere el stock y si puede suma 1 */
        if (e.target.classList.contains("btn-sumar")) {

            /* lee la cantidad actual */
		    let cantidad = parseInt(input.value);
		    /* lee el máximo permitido del stock */
            let max = parseInt(input.max);
            /* busca el mensaje oculto cuando se supera el stock */
		    const stockMsg = fila.querySelector(".stock-msg");

            /* si no supera el stock */
		    if (cantidad < max) {

		        cantidad++;
                /* se actualiza la cantidad del producto */
		        actualizar(itemId, cantidad);
                
		    } 

            else {

        		/* Mostrar mensaje cuando llega al máximo*/
		        stockMsg.classList.remove("d-none");
                /*muestra el mensaje por 2.5 segundos*/
		        setTimeout(() => {
		            stockMsg.classList.add("d-none");
		        }, 2500);
		    }
		}

       /* cuando se da clic en restar. reduce la cantidad y nunca puede ser menor que 1 */
        if (e.target.classList.contains("btn-restar")) {
            /* lee la cantidad actual */
            let cantidad = parseInt(input.value);

            /* si la cantidad es mayor a 1 */
            if (cantidad > 1) {
                cantidad--;
                /* se actualiza la cantidad del producto */
                actualizar(itemId, cantidad);
            }
        }

        /* botón eliminar del carrito, elimina la fila, actualiza el total y el contador */
        if (e.target.classList.contains("btn-eliminar")) {
            /* petición del servidor a través del método POST */
            fetch(`/carrito/eliminar/${itemId}/`, {
                method: "POST",
                headers: { 
                    /* Token de seguridad */
                    "X-CSRFToken": getCookie("csrftoken"),
                }
            })
            .then(res => res.json())
            /* respuesta del servidor */
            .then(data => {
                if (data.success) {
                    /* si todo es correcto elimina la fila */
                    fila.remove();
                    /* actualiza el total */
                    // totalGeneral.textContent = data.total;
                    actualizarTotalEnPantalla(data.total);

                    const contador = document.getElementById("carrito-contador");

                    if (data.total_items > 0) {
                        /* actualiza el contador del carrito */
                        contador.textContent = data.total_items;
                    } else {
                        /* se oculta */
                        contador.style.display = "none";
                    }
                }
            });
        }

    });

    /* si el usuario escribe la cantidad de forma manual */
    document.addEventListener("change", function(e){
        /* se ejecuta cuando se cambie la cantidad */
        if (!e.target.classList.contains("cantidad-input")) return;
         /* busca donde fue el evento (busca la fila) */
        const fila = e.target.closest("tr");
        /* obtiene el id del producto */
        const itemId = fila.dataset.id;
        /* lee el máximo permitido del stock */
        const max = parseInt(e.target.max);
        /* lee la cantidad que ingreso el usuario */
        let cantidad = parseInt(e.target.value);

        /* si se ingresa algo diferente a un numero o es negativo lo cambia por un 1 */
        if (isNaN(cantidad) || cantidad < 1) {
            cantidad = 1;
        }

        /* si la cantidad supera el stock */
        if (cantidad > max) {
            /* ajusta la cantidad solicitada a la cantidad maxima del stock */
		    cantidad = max;
            /* busca el mensaje oculto cuando se supera el stock */
		    const stockMsg = fila.querySelector(".stock-msg");
            /* Mostrar mensaje cuando llega al máximo*/
		    stockMsg.classList.remove("d-none");
            /* se carga el mensaje por 2.5 seg */
		    setTimeout(() => {
		        stockMsg.classList.add("d-none");
		    }, 2500);
		}

        e.target.value = cantidad;
        /* actualiza la cantidad */
        actualizar(itemId, cantidad);

    });

    /* funciona actualiza la cantidad */
    function actualizar(id, cantidad){
    /* se llama a la vista de actualizar d Django enviando el id del producto */
    fetch(`/actualizar/${id}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/x-www-form-urlencoded"
        },
        /* se envía la nueva cantidad */
        body: `cantidad=${cantidad}`
    })
    .then(res => res.json())
    .then(data => {
        const fila = document.querySelector(`tr[data-id='${id}']`);
        if (!fila) return; // Evita romper todo

        const input = fila.querySelector(".cantidad-input");
        const stockMsg = fila.querySelector(".stock-msg");
        const subtotalCell = fila.querySelector(".subtotal");
            
        // const fila = document.querySelector(`tr[data-id='${id}']`);
        // const input = fila.querySelector(".cantidad-input");
        // const stockMsg = fila.querySelector(".stock-msg");

        if (data.success) {

            input.value = cantidad;
            /* se actualiza el subtotal */
             if (subtotalCell) {
            subtotalCell.textContent = "$" + data.subtotal;
        }
            // fila.querySelector(".subtotal").textContent = "$" + data.subtotal;
            /* se actualiza el total */
            // document.querySelector(".total-general").textContent = data.total;
            actualizarTotalEnPantalla(data.total);
            // Oculta mensaje si estaba visible
            if (stockMsg) {
            stockMsg.classList.add("d-none");
        }
            // stockMsg.classList.add("d-none");

        } else {

            // Mostrar mensaje de stock
           	// stockMsg.classList.remove("d-none");

            // Opcional: volver al máximo permitido
            // input.value = input.max;
             if (stockMsg) {
            stockMsg.classList.remove("d-none");
            }

            if (input) {
                input.value = input.max;
            }
            
        }
    });
}

    /* funcion para obtener el token de seguridad de Django */
    function getCookie(name) {
        /* se crea la variable cookievalue */
        let cookieValue = null;
        /* si existen cookies guardadas en el navegador */
        if (document.cookie) {
            /* selecciona todas las cookies las separa con ; y las recorre*/
            document.cookie.split(';').forEach(cookie => {
                /* se eliminan los espacios */
                cookie = cookie.trim();
                /* busca coincidencias de la cookie a buscar con las de la lista*/
                if (cookie.startsWith(name + '=')) {
                    /* se extrae el valor de la cookie */
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                }
            });
        }
        return cookieValue;
    }

    function actualizarTotalEnPantalla(total) {
        document.querySelectorAll(".total-general").forEach(el => {
            el.textContent = total;
        });
    }

    

});