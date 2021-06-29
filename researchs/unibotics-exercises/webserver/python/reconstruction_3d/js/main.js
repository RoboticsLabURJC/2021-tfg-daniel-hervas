var imgL;
var imgR;

function init() {
    imgL = document.getElementById("imageL");
    imgR = document.getElementById("imageR");
    webGLStart();
    websocketClient(wsUri);
}
