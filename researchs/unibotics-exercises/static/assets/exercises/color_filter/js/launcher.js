var ws_manager = "";

function startSim(websocket_address="",server="", username=""){
    if (websocket_address == "") {
		var address_code = "ws://" + server + ":8000/ws/code/" + username + "/";
		var address_gui = "ws://" + server + ":8000/ws/gui/" + username + "/";
		var address_manager = "ws://"+ server + ":8000/ws/localsim/" + username + "/";
	} else {
		is_local = true
		var address_code = "ws://" + websocket_address + ":1905";
		var address_gui = "ws://" + websocket_address + ":2303";
		var address_manager = "ws://" + websocket_address + ":8765";

		/*var websocket_code = new WebSocket("ws://" + websocket_address + ":1905/");*/
	}
    ws_manager = new WebSocket(address_manager);
    exercise = "color_filter"
    websockets_connected = false;

    ws_manager.onopen = function(event){
        set_launch_level(1);
        ws_manager.send(JSON.stringify({"command": "exit", "exercise": ""}));
        ws_manager.send(JSON.stringify({"command": "open", "exercise": exercise}));
        set_launch_level(2);
        ws_manager.send(JSON.stringify({"command" : "Pong"}));
    }

    ws_manager.onmessage = function(event){
        //console.log(event.data);
        if (event.data.level > get_launch_level()) {
            set_launch_level(event.data.level);
        }
        if (event.data.includes("Ping")) {
            if (!websockets_connected && event.data == "Ping3") {
                set_launch_level(4);
                websockets_connected = true;
                declare_code(address_code);
                declare_gui(address_gui);
                setIframe();
            }
            setTimeout(function () {
                ws_manager.send(JSON.stringify({"command" : "Pong"}));
            }, 1000)
        }
    }
}