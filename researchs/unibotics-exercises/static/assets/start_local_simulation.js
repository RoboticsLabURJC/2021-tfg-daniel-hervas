var websocket_docker;

function startSimulation(server, username, websocket_address="") {
	console.log("START LOCAL SIM", websocket_address, server)
	if (websocket_address == "") {
		websocket_docker = new WebSocket("ws://"+ server + ":8000/ws/localsim/" + username + "/open/");
	} else {
		websocket_docker = new WebSocket("ws://" + websocket_address + ":8765");
	}

	websocket_docker.onopen = function (event) {
		if (websocket_address != "") {
			console.log("Conectado al docker manager");
			websocket_docker.send("open");
		}
	}
	websocket_docker.onclose = function (event) {
		if (event.wasClean) {
		    console.log("Sending close sim");
		} else {
			console.log("Close manager")
		}
	}

}

function stopSimulation(server, username, websocket_address="") {
	console.log("STOP LOCAL SIM", websocket_address)
	if (websocket_address == "") {
		websocket_docker = new WebSocket("ws://" + server + ":8000/ws/localsim/" + username +  "/close/");
	} else {
		websocket_docker = new WebSocket("ws://" + websocket_address + ":8765");
	}
	websocket_docker.onopen = function (event) {
		console.log("Conectado al docker");
		if (websocket_address != "") {
			console.log("Conectado al docker manager");
			websocket_docker.send("close");
		}
	}

	websocket_docker.onclose = function (event) {
		if (event.wasClean) {
		    console.log("Sending close sim");
		} else {
			console.log("Close manager")
		}
	}

}