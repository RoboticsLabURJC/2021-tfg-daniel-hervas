//Editor Part
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/python");

var stop_button = document.getElementById("stop");
stop_button.disabled = true;
stop_button.style.opacity = "0.4";
stop_button.style.cursor = "not-allowed";

// running variable for psuedo decoupling
// Play/Pause from Reset
var frequency = "0",
	running = false;

//WebSocket for Code
var websocket_code_guest;
function declare_code_guest(websocket_address){
	console.log('CODE WS ADDRESS:',websocket_address);
	websocket_code_guest = new WebSocket(websocket_address);

	websocket_code_guest.onopen = function(event){
		//alert("[open] Connection established!");
		set_launch_level(get_launch_level()+1);
	}
	websocket_code_guest.onclose = function(event){
		if(event.wasClean){
			alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		}
		else{
			alert("[close] Guest Connection closed!" + event);
		}
	}

	websocket_code_guest.onmessage = function(event){
		var source_code = event.data;
		operation = source_code.substring(0, 5);

		if(operation == "#load"){
			editor.setValue(source_code.substring(5,));
		}else if(operation == "#freq"){
		 	var frequency_message = JSON.parse(source_code.substring(5,));
		 	// Parse GUI and Brain frequencies
		 	document.querySelector("#ideal_gui_frequency").value = frequency_message.gui;
		 	document.querySelector('#ideal_code_frequency').value = frequency_message.brain;
		 	document.querySelector('#real_time_factor').value = frequency_message.rtf;
		}
		// Send the acknowledgment message along with frequency
		code_frequency = document.querySelector('#code_freq').value;
		gui_frequency = document.querySelector('#gui_freq').value;
		real_time_factor = document.querySelector('#real_time_factor').value;
		
		frequency_message = {"brain": code_frequency, "gui": gui_frequency, "rtf": real_time_factor};
		websocket_code_guest.send("#freq" + JSON.stringify(frequency_message));
	};
}

// Function that send/submits an empty string
function stopCode(){
    var stop_code = "#paus";
    console.log("Message sent!");

	websocket_code_guest.send(stop_code);

	running = false;
	try {
		pause_lap()
	}
	catch {

	}
}

function saveCode(exercise){
	// Get the code from editor and add header
	
	var python_code = editor.getValue();
	python_code = "#save" + python_code;
	console.log("Code Sent! Check terminal for more information!");
	websocket_code_guest.send(python_code)
}


// Function to load the code
function loadCode(){
	// Send message to initiate load message
	var message = "#load";
	websocket_code_guest.send(message);

}

// Function to command the simulation to reset
function resetSim(){
	// Send message to initiate reset
	var message = "#rest"
	websocket_code_guest.send(message)
	try {
    	reset_gui()
	}
	catch {

	}
	if(running == true){
		submitCode();
	}
}