// Retreive the canvas elements and context
var mapCanvas = document.getElementById("birds-eye"),
    ctx = mapCanvas.getContext("2d");

// Function to draw triangle
// Given the coordinates of center, and
// the angle towards which it points
function drawCircles(x_host, y_host, x_guest, y_guest){
	let text;

	ctx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);
	
	// Draw checkpoints
	drawCheckpoints(checkpoints);
	
	// Draw HOST
	ctx.beginPath();
	ctx.arc(x_host, y_host, 2, 0, 2 * Math.PI);
	ctx.fillStyle = "red";
	text = "HOST "+Math.round(x_host)+','+Math.round(y_host);
	ctx.fillText(text, x_host, y_host);
	ctx.closePath();
	
	ctx.lineWidth = 1.5;
	ctx.strokeStyle = "#666666";
	ctx.stroke();
	
	ctx.fillStyle = "#FF0000";
	ctx.fill();

	// Draw guest
	ctx.beginPath();
	ctx.arc(x_guest, y_guest, 2, 0, 2 * Math.PI);
	ctx.fillStyle = "green";
	text = "GUEST "+Math.round(x_guest)+','+Math.round(y_guest);
	ctx.fillText(text, x_guest, y_guest);
	ctx.closePath();
	
	ctx.lineWidth = 1.5;
	ctx.strokeStyle = "#666666";
	ctx.stroke();
	
	ctx.fillStyle = "#46ff03";
	ctx.fill();
}

function drawCheckpoints(arr){
	arr.forEach(e => {
		ctx.beginPath();
		ctx.arc(e[1], e[2], 2, 0, 2 * Math.PI);
		ctx.closePath();
		
		// Style
		ctx.lineWidth = 1.5;
		ctx.strokeStyle = "#666666";
		ctx.stroke();
		
		ctx.fillStyle = "#003EFE";
		ctx.fill();
	});
}