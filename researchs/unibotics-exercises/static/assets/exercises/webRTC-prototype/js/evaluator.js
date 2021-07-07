var start_pos = [12,63]

var n = 0;
var point = 0;
var lap = 0;


const reset = document.getElementById("reset");

reset.addEventListener("click", function(){
  document.getElementById('porcentaje_bar').innerHTML = 0 +'%';
  document.getElementById('porcentaje_bar').style.width = 0+'%';
  n = 0;
  point = 0;
  lap = 0;
});



//gui.js data 
function Evaluator(content){
   var x = Math.round(content[0])
   var y = Math.round(content[1])
   //console.log(x,y)
   //console.log(checkpoints[n][1],checkpoints[n][2])
   var d = Math.sqrt(Math.pow((checkpoints[n][1]-x), 2)+Math.pow((checkpoints[n][2]-y), 2));
   var d1 = Math.sqrt(Math.pow((checkpoints[n][1]+5-x), 2)+Math.pow((checkpoints[n][2]+5-y), 2));
   var d2 = Math.sqrt(Math.pow((checkpoints[n][1]-5-x), 2)+Math.pow((checkpoints[n][2]-5-y), 2));
   var d3 = Math.sqrt(Math.pow((checkpoints[n][1]+5-x), 2)+Math.pow((checkpoints[n][2]-5-y), 2));
   var d4 = Math.sqrt(Math.pow((checkpoints[n][1]-5-x), 2)+Math.pow((checkpoints[n][2]+5-y), 2));
   //console.log(d)
   //console.log(n)
   if (d <= 10 || d1 <= 15 || d2 <= 15 || d3 <= 15 || d4 <= 15){
       n+=1
     if(n >= 60){
       lap+= 1
       console.log("vuelta finalizada", lap)
       var lap_time_display = document.getElementById("lap_time").textContent;
       document.getElementById('lap').innerHTML += 'Lap ' + lap + ' ' + lap_time_display+'<br>';
       document.getElementById('porcentaje_bar').innerHTML = 100 +'%';
       document.getElementById('porcentaje_bar').style.width = 100+'%';

     }
   }
   var porcentaje= document.getElementById('evaluator')
   var progress_bar = Math.round(n/checkpoints.length*100)
//  porcentaje.innerHTML= 'Pocentaje' + Math.round(n/checkpoints.length*100) +'%'

  if (n!=60){
    document.getElementById('porcentaje_bar').innerHTML = progress_bar +'%';
    document.getElementById('porcentaje_bar').style.width = progress_bar+'%';
  }else{
    n=0;
  }

 }
