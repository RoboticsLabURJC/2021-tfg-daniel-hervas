

function websocketClient(wsUri) {
    websocket = new WebSocket(wsUri);
    
    websocket.onopen = function(evt) {
        onOpen(evt)
    };

    websocket.onmessage = function(evt) {
        onMessage(evt)
    };

    websocket.onerror = function(evt) {
        console.error(evt.data);
    };

    websocket.onclose = function (evt) {
    // Connection closed.
    // Firstly, check the reason.
    
        if (evt.code != 1000) {
            onError(evt);
        }
    }
}

function onOpen(evt) {
    console.log("CONNECTED");
}




/******* Communications ******
points: {func: drawPoints, data: [PointRGB, PointRGB,...], refresh: True/False}
Matches: {func: matches, data: string (image in base64 format)}
Image filtered: {func: imageF, data: string (image in base64 format)}

Note:
PointRGB = {x, y, z, r, g, b}
*/
function onMessage(evt) {
    msg = JSON.parse(evt.data);
    switch(msg.func) {
        case "drawPoints":
            if (msg.refresh){
                deleteObj("points");
            }
            points =msg.data;
            for (var i = 0; i < points.length; i+=1) {
                addPoint(points[i]);
            }
            break;
        case "matches":
            imgL.src = msg.data;
            break;

        case "imageF":
            imgR.src = msg.data;
            break;
        default:
            console.error("wrong func: "+ msg.func)
    }
}


function onError(evt) {
    console.error(evt);
    console.log("ERROR");
    setTimeout(function() {
        websocketClient(wsUri);
    }, 500);

}

function doSend(message) {
    writeToScreen("SENT: " + message); websocket.send(message);
}


//window.addEventListener("load", init, false);
