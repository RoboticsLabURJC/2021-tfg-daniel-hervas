// Set the src of iframe tag
//document.getElementById("gzweb").setAttribute(
//	"src", "http://" + websocket_address + ":8080")

// To decode the image string we will receive from server
function decode_utf8(s) {
	return decodeURIComponent(escape(s))
}

// Websocket and other variables for image display
var websocket_gui, animation_id;
var image_data, source, shape;
var lap_time, pose, content;
var pose_guest, content_guest;
var command_input;
var checkpoints=circuit_checkpoints;

function declare_gui(websocket_address) {
	websocket_gui = new WebSocket(websocket_address);

	websocket_gui.onopen = function (event) {
		//alert("[open] Connection established!");
		set_launch_level(get_launch_level()+1);
	}

	websocket_gui.onclose = function (event) {
		$("#connection-button").removeClass("btn-success").addClass("btn-danger");
		$("#connection-button").html('<span id="loading-connection" class="bi bi-arrow-down-up"></span> Connect');
		$("#connection-button").prop('disabled', false);
		
		if (event.wasClean) {
			//alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		}
		else {
			//alert("[close] Connection closed!");
		}
	}

	// What to do when a message from server is received
	websocket_gui.onmessage = function (event) {
		checkpoints = circuit_checkpoints

		var path = checkpoints;
		let values;
		let distance_host_element = $('.distance-host');
		let distance_guest_element = $('.distance-guest');

		operation = event.data.substring(0, 4);
		$("#connection-button").removeClass("btn-warning").addClass("btn-success");
		$("#connection-button").html('<span id="loading-connection" class="bi bi-arrow-down-up"></span> Connected');
		$("#connection-button").prop('disabled', true);

		if (operation == "#gui") {
			// Parse the entire Object
			data = JSON.parse(event.data.substring(4,));

			// Parse the Image Data
			image_data = JSON.parse(data.image),
				source = decode_utf8(image_data.image),
				shape = image_data.shape;

			//console.log(image_data, image_data_guest);

			if (source != "") {
				canvas.src = "data:image/jpeg;base64," + source;
				canvas.width = shape[1];
				canvas.height = shape[0];
			}

			// // Parse the Lap data
			// lap_time = data.lap;
			// if (lap_time != "") {
			// 	lap_time_display.textContent = lap_time;
			// }

			// Parse the Map data
			// Slice off ( and )
			// Position Host
			pose = data.map.substring(1, data.map.length - 1);
			//console.log('HOST: ', pose);
			content = pose.split(',').map(function (item) {
				return parseFloat(item);
			})

			// Position Guest
			pose_guest = data.map_guest.substring(1, data.map_guest.length - 1);
			//console.log('GUEST: ', pose_guest);
			content_guest = pose_guest.split(',').map(function (item) {
				return parseFloat(item);
			})

			//Evaluator(content);			// Host
			drawCircles(content[0], content[1], content_guest[0], content_guest[1]);
			//drawOdometry(data.v, data.w);

			// Get closest checkpoints
			close_host = getClosestCheckpoint(content, path);
			close_guest = getClosestCheckpoint(content_guest, path);
			
			// Get path to reach the checkpoints
			values = getNewPath(content, content_guest,close_host, close_guest);
			path = values.path;
			arr_pos_host = values.pos_host;
			arr_pos_guest = values.pos_guest;
			console.log(checkpoints);
			//console.log(checkpoints, arr_pos_host, arr_pos_guest);

			// console.log('HOST->GUEST: ', getDistanceOriginDest(arr_pos_host, arr_pos_guest, path));
			// console.log('GUEST->HOST: ', getDistanceOriginDest(arr_pos_guest, arr_pos_host, path));

			// Get distances and set them too
			distance_host_element = $('.distance-host').text(getDistanceOriginDest(arr_pos_host, arr_pos_guest, path));
			distance_guest_element = $('.distance-guest').text(getDistanceOriginDest(arr_pos_guest, arr_pos_host, path));

			// Send the Acknowledgment Message
			websocket_gui.send("#ack");
		}

		else if (operation == "#cor") {
			// Set the value of command
			command_input = event.data.substring(4,);
			command.value = command_input;
			// Go to next command line
			next_command();
			// Focus on the next line
			command.focus();
		}
	}
}

var canvas = document.getElementById("gui_canvas");
//var canvas_guest = document.getElementById("gui_canvas_guest");

// // Lap time DOM
// var lap_time_display = document.getElementById("lap_time");

function pause_lap(){
	websocket_gui.send("#paus");
}

function unpause_lap(){
	websocket_gui.send("#resu");
}

function reset_gui(){
	websocket_gui.send("#rest");
}