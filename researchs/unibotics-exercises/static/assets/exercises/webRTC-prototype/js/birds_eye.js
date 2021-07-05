// Retreive the canvas elements and context
var mapCanvas = document.getElementById("birds-eye"),
    ctx = mapCanvas.getContext("2d");

// Function to draw triangle
// Given the coordinates of center, and
// the angle towards which it points
function drawCircles(x_host, y_host, x_guest, y_guest){
	ctx.clearRect(0, 0, mapCanvas.width, mapCanvas.height);	
	
	//cursor_x = x;
	//cursor_y = y;
	
	// Draw HOST
	ctx.beginPath();
	ctx.arc(x_host, y_host, 2, 0, 2 * Math.PI);
	ctx.arc(x_guest, y_guest, 2, 0, 2 * Math.PI);
	ctx.closePath();
	
	ctx.lineWidth = 1.5;
	ctx.strokeStyle = "#666666";
	ctx.stroke();
	
	ctx.fillStyle = "#FF0000";
	ctx.fill();

	// Draw guest
	ctx.beginPath();
	ctx.arc(x_guest, y_guest, 2, 0, 2 * Math.PI);
	ctx.closePath();
	
	ctx.lineWidth = 1.5;
	ctx.strokeStyle = "#666666";
	ctx.stroke();
	
	ctx.fillStyle = "#46ff03";
	ctx.fill();


}