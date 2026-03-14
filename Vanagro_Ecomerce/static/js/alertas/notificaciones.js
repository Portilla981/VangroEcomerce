function activarNotificaciones(){

const notificaciones=document.querySelectorAll(".notificacion")

notificaciones.forEach((noti)=>{

    if(noti.dataset.activa) return

    noti.dataset.activa="true"

    setTimeout(()=>{

        noti.style.opacity="0"
        noti.style.transform="translateX(50px)"

        setTimeout(()=>{
            noti.remove()
        },400)

    },4000)

})

}

document.addEventListener("DOMContentLoaded",activarNotificaciones)