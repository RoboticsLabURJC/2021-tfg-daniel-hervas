'use strict';

document.addEventListener('onroomnameset', function(){
    if(!setstream){
        streamws = new WebSocket(
            'ws://' +
            '127.0.0.1:8000' +
            '/ws/stream/' +
            streamroom +
            '/'
        );

        streamws.onmessage = function(e){
            let message_data = JSON.parse(event.data);
            console.log('[PARENT] streamws: ', message_data);
            if(message_data['type'] == 'checkusers'){
                if(message_data['users']){
                    console.log('[PARENT] usuarios correctos');
                    iframe.contentWindow.postMessage('start', '*');
                }else{
                    console.log('[PARENT] usuarios incorrectos');
                }
            }else if(message_data['type'] == 'candidate'){
                console.log('[PARENT] Candidate received');
                addIceCandidate(message_data['candidate']);
            }else if(message_data['type'] == 'offer'){
                console.log('[PARENT] Offer received');
                startRemoteStream(message_data['offer']);
            }else if(message_data['type'] == 'answer'){
                console.log('[PARENT] Answer received');
                setAnswerDescription(message_data['answer']);
            }else if(message_data['type'] == 'denied'){
                console.log('[PARENT] Denied connection');
                window.location.pathname = '/';
            }
        };
        setstream = true;
    }
});

// Event listener para recibir la sala
window.addEventListener('message', function(e){
    let message = JSON.parse(e.data);
    console.log('[PADRE] mensaje: ', e.data);
    if(message['stream']){
        console.log('[PADRE] sala stream: ', message['stream']);
        // ENviar websocket al otro extremo
        websocket.send(JSON.stringify({
            'type':'stream',
            'stream':message['stream']
        }));
    }
});