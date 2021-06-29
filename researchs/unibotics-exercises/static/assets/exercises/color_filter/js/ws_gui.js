

// To decode the image string we will receive from server
function decode_utf8(s){
    return decodeURIComponent(escape(s))
}

// Websocket and other variables for image display
var websocket_gui, animation_id;

function declare_gui(websocket_address){
	websocket_gui = new WebSocket(websocket_address);

	websocket_gui.onopen = function(event){
		//alert("[open] Connection established!");
		set_launch_level(get_launch_level()+1);
	}

	websocket_gui.onclose = function(event){
		$("#connection-button").removeClass("btn-success").addClass("btn-danger");
		$("#connection-button").html('<span id="loading-connection" class="bi bi-arrow-down-up"></span> Connect');
		$("#connection-button").prop('disabled', false);

		if(event.wasClean){
			//alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		}
		else{
			//alert("[close] Connection closed!");
		}
	}

	// What to do when a message from server is received
	websocket_gui.onmessage = function(event){
		operation = event.data.substring(0, 4);
		$("#connection-button").removeClass("btn-warning").addClass("btn-success");
		$("#connection-button").html('<span id="loading-connection" class="bi bi-arrow-down-up"></span> Connected');
		$("#connection-button").prop('disabled', true);

		if(operation == "#gui"){
			// Parse the entire Object
			var data = JSON.parse(event.data.substring(4, ));
			
			// Parse the Image Data
			var image_data = JSON.parse(data.image),
				source = decode_utf8(image_data.image),
				shape = image_data.shape;
			
			if(source != ""){
				image.src = "data:image/jpeg;base64," + source;
				canvas.width = shape[1];
				canvas.height = shape[0];
			}
			
			// Send the Acknowledgment Message
			websocket_gui.send("#ack");
		}
		
	}
}

var canvas = document.getElementById("gui_canvas"),
    context = canvas.getContext('2d');
    image = new Image();


// For image object
image.onload = function(){
    update_image();
}
// Request Animation Frame to remove the flickers
function update_image(){
	animation_id = window.requestAnimationFrame(update_image);
	context.drawImage(image, 0, 0);
}
