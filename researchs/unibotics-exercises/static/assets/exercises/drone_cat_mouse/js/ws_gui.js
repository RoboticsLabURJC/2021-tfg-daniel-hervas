// Set the src of iframe tag
//document.getElementById("gzweb").setAttribute(
//	"src", "http://" + websocket_address + ":8080")

// To decode the image string we will receive from server
function decode_utf8(s){
    return decodeURIComponent(escape(s))
}

// Websocket and other variables for image display
var websocket_gui;

function declare_gui(websocket_address){
	websocket_gui = new WebSocket( websocket_address);

	websocket_gui.onopen = function(event){
		alert("[open] Connection established!");
		set_launch_level(get_launch_level()+1);
	}
	
	websocket_gui.onclose = function(event){
		if(event.wasClean){
			alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		}
		else{
			alert("[close] Connection closed!");
		}
	}

	// What to do when a message from server is received
	websocket_gui.onmessage = function(event){
		$("#connection-button").removeClass("btn-warning").addClass("btn-success");
		$("#connection-button").html('<span id="loading-connection" class="bi bi-arrow-down-up"></span> Connected');
		$("#connection-button").prop('disabled', true);
		var operation = event.data.substring(0, 4);
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

		if(operation == "#gul"){
			// Parse the entire Object
			var data = JSON.parse(event.data.substring(4, ));

			// Parse the Image Data
			var image_data = JSON.parse(data.image),
				source = decode_utf8(image_data.image),
				shape = image_data.shape;

			if(source != ""){
				image_left.src = "data:image/jpeg;base64," + source;
				canvas_left.width = shape[1];
				canvas_left.height = shape[0];
			}

			// Send the Acknowledgment Message
			websocket_gui.send("#ack");
		}
	
		
	}
}

// Function to start mouse
function playmouse(){
    // Send message to initiate start mouse
    var message = "#mou" + document.getElementById('mouse').value;
    console.log("Message sent: " + message);
    websocket_gui.send(message);
}

// Function to takeoff mouse
function stopmouse(){
    // Send message to initiate start mouse
    var message = "#stp";
    console.log("Message sent: " + message);
    websocket_gui.send(message);
}

// Function to land mouse
function resetmouse(){
    // Send message to initiate start mouse
    var message = "#rst";
    console.log("Message sent: " + message);
    websocket_gui.send(message);
}

var canvas = document.getElementById("gui_canvas_right"),
    context = canvas.getContext('2d');
    image = new Image();
var canvas_left = document.getElementById("gui_canvas_left"),
    context_left = canvas_left.getContext('2d')
    image_left = new Image();

// For image object
image.onload = function(){
    update_image();
}

// For image object
image_left.onload = function(){
    update_left_image();
}

// Request Animation Frame to remove the flickers
function update_image(){
	window.requestAnimationFrame(update_image);
	context.drawImage(image, 0, 0);
}

// Request Animation Frame to remove the flickers
function update_left_image(){
	window.requestAnimationFrame(update_left_image);
	context_left.drawImage(image_left, 0, 0);
}
