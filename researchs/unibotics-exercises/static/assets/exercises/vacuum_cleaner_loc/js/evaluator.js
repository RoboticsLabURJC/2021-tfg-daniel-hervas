//black_squares  
var canvas = document.getElementById("grid");
var squares = [];
var sizeSquare = {w: 10, h: 10};
var color = "";
var inputColor = document.getElementById("color");
var score = document.getElementById("score");
var count = 0;
var fill_index=[];
const room_total_squares = 224;

function Load(){
//Drawing canvas grid for first time
    var canvas = document.getElementById("grid");
    if (canvas && canvas.getContext) {
        var ctx = canvas.getContext("2d");
        if (ctx) {
            function dibujaGrid(disX, disY, wLine, color){
	        squares=[];
                ctx.strokeStyle = color;
                ctx.lineWidth = wLine;
                var columnas = [];
                var filas = [];
                for (i = 0; i < canvas.width; i += disX) {
                    ctx.moveTo(i, 0);
                    ctx.lineTo(i, canvas.height);
                    columnas.push(i);
		    //console.log(columnas)
                }
                for (i = 0; i < canvas.height; i += disY) {
                    ctx.moveTo(0, i);
                    ctx.lineTo(ctx.canvas.width, i);
                    filas.push(i);
                }
		ctx.stroke();
                columnas.push(0);
                filas.push(0);
                for (x = 0; x < columnas.length; x++) {
                    for (y = 0; y < filas.length; y++) {
                        squares.push([columnas[x], filas[y], disX, disY]);

                    }
                }
		//console.log(squares)

            }

            function fillCell(x, y) {
                color = inputColor.value;
                ctx.fillStyle = "#000000";
                for (i = 0; i < squares.length; i++) {
                    var square = squares[i];
                    if (
                        x > square[0] &&
                        x < square[0] + square[2] &&
                        y > square[1] &&
                        y < square[1] + square[3]
                    ) {
			
                        ctx.fillRect(square[0], square[1], sizeSquare.w, sizeSquare.h);
			 break;
                    }
                }
            }
            dibujaGrid(sizeSquare.w, sizeSquare.h, 1, "#44414B");

        } else {
            alert("No se pudo cargar el contexto");
        }
    }
}

  
window.onload = function (){
    Load();
    var canvas = document.getElementById("grid");
    var ctxto = canvas.getContext("2d");

    for (k = 0; k < black_squares.length; k++) {
        var color = '#000000';
        fillCell(black_squares[k][0], black_squares[k][1],ctxto, color);
    }
    count=0
    fill_index =[]
	
};
           

 function fillCell(x, y,ctx,color) {

                ctx.fillStyle = color;
                for (i = 0; i < squares.length; i++) {
                    var square = squares[i];
                    if (
                        x > square[0] &&
                        x < square[0] + square[2] &&
                        y > square[1] &&
                        y < square[1] + square[3]
                    ) {
			
                        ctx.fillRect(square[0], square[1], sizeSquare.w, sizeSquare.h);
			
			if (! fill_index.includes(i)){
				fill_index.push(i);
				count= count + 1;
			}
			
                        break;
                    }
                }
                
		//console.log(squares)
            }

function Evaluator(x,y){
    var canvas = document.getElementById("grid");
    var ctx = canvas.getContext("2d");
	
    color= '#0000FF';
    const reset = document.getElementById("reset");
    reset.addEventListener("click", function(){

	var canvas = document.getElementById("grid");
        var ctx = canvas.getContext("2d");
	
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        Load();
	var canvas = document.getElementById("grid");
	var ctxto = canvas.getContext("2d");
	color = '#000000';
	for (k = 0; k < black_squares.length; k++) {
	    
            fillCell(black_squares[k][0], black_squares[k][1],ctxto, color);
        }
	count=0
	fill_index =[]

    });
 
    //console.log(count);
    score.innerHTML=Math.round((count / room_total_squares) *100);

    fillCell(x,y, ctx,color)
		
}

