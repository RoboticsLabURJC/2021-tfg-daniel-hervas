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
    /**var editor = ace.edit("ace");**/
     var pythonCodeString = editor.getValue();
        const request = new Request('/academy/evaluate_py_style/'+ exercise +'/', {method: 'POST', body: '{"python_code": "' + pythonCodeString +'"}'});
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
  };

function saveCodeUnibotics(exercise){
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
	   	 console.log("ENTRA ONLINE");
	   	 alert("Your code has been saved")
	   } else{
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

function loadCodeLocally(){
	    const realFileBtn = document.getElementById("real-file");
    	const customBtn = document.getElementById("load");
    	const editorele = ace.edit("editor");
    	customBtn.addEventListener("click", function(){
    		realFileBtn.click();
    	});
    	realFileBtn.addEventListener("change", function() {
    		if (realFileBtn.value) {
    			console.log("FILE CHOSEN:");
    			console.log(realFileBtn.value);
    			var fr = new FileReader();
    			fr.onload = function(){
    				editorele.setValue(fr.result, 1);
    			}
    			fr.readAsText(this.files[0]);

    		}
    	});
}

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
