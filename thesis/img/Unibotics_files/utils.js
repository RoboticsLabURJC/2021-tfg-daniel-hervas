function get_inner_size(element) {
  var cs = getComputedStyle(element);
  var padding_x = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
  var padding_y = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);

  var border_x = parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth);
  var border_y = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth);

  // Element width and height minus padding and border
  width = element.offsetWidth - padding_x - border_x;
  height = element.offsetHeight - padding_y - border_y;

  return {width: Math.floor(width), height: Math.floor(height)};
}

function get_novnc_size() {
  var inner_size = get_inner_size(document.querySelector(".split.b"));
  var width = inner_size.width || document.body.clientWidth;
  // Since only 50% of height is used for gazebo iframe
  var height = Math.floor(0.5 * inner_size.height) || document.body.clientHeight;
  return {width: width, height: height};
}

function evaluate_code(exercise){
  let python_code = editor.getValue();
	python_code = "#code\n" + python_code;
  if (websocket_code != null && websocket_gui != null && websocket_code.readyState == 1 && websocket_gui.readyState == 1) {
    ws_manager.send(JSON.stringify({"command": "evaluate_style", "code": python_code}));
    } else {
    alert('The connection must be established before evaluating the code.');
  }
  var pythonCodeString = editor.getValue();
  const request = new Request('/academy/evaluate_py_style/'+ exercise +'/', {method: 'POST', body: '{"python_code": "' + pythonCodeString +'"}'});
  /*
  fetch(request)
    .then(response => response.text())
    .catch(error => {
      console.error(error);
    }).then(function(result){
      result = "Evaluación del estilo:\n\n" + result ;
      console.log(result);
      jQuery.noConflict();
      jQuery('#evalModal').modal({
          backdrop: false,
          keyboard: false,
          focus: false,
     show: true,
    });

      jQuery('#evalModal').css({
  "position": "relative"
      });
jQuery('#evalModal').find('.modal-body').text(result);
    jQuery('.modal-dialog').draggable({
          handle: ".modal-header"
      });
    jQuery('.modal-dialog').css({
          "position": "fixed",
  "margin-left": "50%"
      });


    });
    */
};

function downloadUserCode(exercise) {
  const request = new Request('/academy/exercise/reload_code/' + exercise + "/");
  fetch(request)
    .then(response => response.text())
    .catch(error => {
     console.error(error);
    }).then(function(result){
      showUserCode(result);
    });
}

function saveCodeUnibotics(exercise, verbose = true){
// Get the code from editor and add header
var python_code = editor.getValue();
console.log("GUARDADO");
/*websocket_data.send(JSON.stringify({"message": "save","code": python_code, "exercise": exercise}))*/
const request = new Request('/academy/exercise/save/'+ exercise +'/', {method: 'POST', headers: {"X-CSRFToken": csrf}, body:python_code});
fetch(request)
  .then(response => response.text())
  .catch(error => {
   console.error(error);
  }).then(function(result){
    console.log("RESULTADO", result);
   if (result=="Online") {
     if (verbose) {
      console.log("ENTRA ONLINE");
      alert("Your code has been saved")
     }
   } else{
     if (verbose)
      console.log("AQUI");
      var blob = new Blob([result], {type: "text/plain; charset=utf-8"});
      if (window.navigator.msSaveOROpenBlob)
  window.navigator.msSaveOrOpenBlob(blob, $("#form29").val());
else{
  var a = document.createElement("a"),
  url = URL.createObjectURL(blob);
  a.href = url;
  a.download = exercise + ".py";
  document.body.appendChild(a);
  a.click()
  setTimeout(function(){
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 0);
  }
   }
   /*alert(result);*/
  });
}

function freeDocker(e){
// Get the code from editor and add header
console.log("LIBERAR");
const request = new Request('/academy/freedocker/');
fetch(request)
  .then(response => response.text())
  .catch(error => {
   console.error(error);
  }).then(function(result){

  });
}

/*
function loadCodeLocally(){
    const realFileButton = document.getElementById("real-file");
    const customBtn = document.getElementById("load");
    const editorele = ace.edit("editor");
    customBtn.addEventListener("click", function(){
      realFileButton.click();
    });
    realFileButton.addEventListener("change", function() {
      if (realFileButton.value) {
        console.log("FILE CHOSEN:");
        console.log(realFileButton.value);
        var fr = new FileReader();
        fr.onload = function(){
          editorele.setValue(fr.result, 1);
        }
        fr.readAsText(this.files[0]);

      }
    });
}
*/

function reload(){
 const request = new Request('/academy/reload_exercise/');
 fetch(request)
   .then(response => response.text())
   .catch(error => {
    console.error(error);
   }).then(function(result){

   });
 }

window.addEventListener("DOMContentLoaded", function (e) {
console.log("Todos los recursos terminaron de cargar!");
var current_location = window.location.href.split('/')
var lastTime = localStorage.getItem('lastTime')
var exercise = localStorage.getItem('exercise')
if(lastTime){
 lastTime = Number(lastTime)
 var now = new Date().getTime();
 var difference = (now - lastTime)
 if (current_location[current_location.length-2]==exercise) {
   if(difference < 3*1000){
     reload()
   }else{
   }
 }
}
});

var efficacy_timer;
var timer_running = false;
var exercise_times = {"follow_line": 6000, "obstacle_avoidance": 5000, "3d_reconstruction": 5000, "drone_cat_mouse": 5000, "vacuum_cleaner": 5000, "vacuum_cleaner_loc": 5000, "global_navigation": 5000, "opticalflow_teleop": 5000};
let ms_time = 0;
try {
  ms_time = exercise_times[exercise];}
  catch (e) {
    ms_time = 1000;
  }
function efficacy_evaluator(exercise){
// If efficacy is not running, record and send data
if (timer_running == false) {
  timer_running = true;
  resetSimulation();
  start();
  // Sets timer to send info
  efficacy_timer = setTimeout(function(){
    if (exercise == 'follow_line') {
      var total_score = document.getElementById("porcentaje_bar").innerHTML
      total_score = total_score.substring(0, total_score.length - 1)
    }else{
      var total_score = document.getElementById("score").innerHTML
    }
    const request = new Request('/academy/efficacy_evaluator/', {method: 'POST', headers: {"X-CSRFToken": csrf}, body: '{"exercise": "'+exercise+'", "score":'+total_score+'}'});
    fetch(request)
      .then(response => response.text())
      .catch(error => {
       console.error(error);
      }).then(function(result){});
    timer_running = false;
    console.log("Socre sent: ", total_score);
  }, ms_time);
} else {  // If efficacy is running, stop
  timer_running = false;
  clearTimeout(efficacy_timer);
  stop();
}
}

// Stops evaluation
function stop_efficacy_evaluator() {
clearTimeout(efficacy_timer);
if (timer_running == true) {
  timer_running = false;
}
}