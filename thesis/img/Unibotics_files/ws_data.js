var websocket_data = "";
function setWebsocketData(server , username) {
    websocket_data = new WebSocket("ws://" + server + ":8000/ws/data/" + username + "/");
};



