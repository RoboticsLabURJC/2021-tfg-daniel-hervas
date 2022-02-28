var inactivity = null;
var deadline = 1000 * 60 * 20;
console.log("CARGA IDLE")

function inactivity_alert() {

    let ultimatum;
    Swal.fire({
          title: '<span style="font-size:25px;">¡Alerta de Inactividad!</span>',
          type: 'warning',
          html: '<span style="font-size:15px;">Tu sesión se cerrará en <b></b> segundos.<br><strong>Presiona el ratón o cualquier tecla para continuar tu sesión.</strong></span>',
          width: 500,
          timer: 10000,
          onBeforeOpen: () => {
                Swal.showLoading();
                ultimatum = setInterval(() => {
                    Swal.getContent().querySelector('b').textContent = Math.round(Swal.getTimerLeft()/1000);
            }, 1000)
    },
    onClose: () => {
        clearInterval(ultimatum);
    }
    }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
            console.log('Inactivity deadline reached.')
            // Expulsar del servidor (cerrar sesión)
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            url = '/academy/logout/inactivity'
            a.href = url;
            a.click();
            window.URL.revokeObjectURL(url)
        }
    });
}

inactivity = setTimeout(inactivity_alert, deadline);

window.onclick = function (event) {
    swal.close();
    console.log(event);
    clearTimeout(inactivity);
    inactivity = setTimeout(inactivity_alert, deadline);
}

window.onkeypress = function (event) {
    swal.close();
    console.log(event);
    clearTimeout(inactivity);
    inactivity = setTimeout(inactivity_alert, deadline);
}
