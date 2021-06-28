'use strict';

// Create websocket for communication
const websocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    room_name +
    '/'
);
console.log('Websocket created for room: ', room_name);

websocket.onmessage = function(event){
    let message_data = JSON.parse(event.data);
    console.log('WebSocket received: ', message_data);

    // If the content type from the websocket is chat_message,
    // the text field is appended to the chat box
    if(message_data['type'] == 'chat_message'){
        console.log('Escribir mensaje');
        add_message('receive', message_data['message']);
    }else if(message_data['type'] == 'candidate'){
        console.log('Candidate received');
        addIceCandidate(message_data['candidate']);
    }else if(message_data['type'] == 'offer'){
        console.log('Offer received');
        startRemoteStream(message_data['offer']);
    }else if(message_data['type'] == 'answer'){
        console.log('Answer received');
        setAnswerDescription(message_data['answer']);
    }else if(message_data['type'] == 'denied'){
        console.log('Denied connection');
        window.location.pathname = '/';
    }else if(message_data['type'] == 'checkusers'){
        if(message_data['users']){
            iframe.contentWindow.postMessage('start', '*');
        }else{
            console.log('No peer connected')
        }
    }else if(message_data['type'] == 'stream'){
        // Conectarse al streamws
        if(!streamcon){
            setStreamRoom(message_data['stream']);
        }
    }
};

function setStreamRoom(name){
    streamroom = name;
    streamcon = true;
    console.log('Conectado al streamws');
    // Throw event
    document.dispatchEvent(onRoomNameSet);
}

function add_message(direction, message){
    let chat_log = document.querySelector('#chat-log');

    if(direction === 'send'){
        chat_log.innerHTML += ('<p class="send"> [You] ' + message + '</p>');
    }else if(direction === 'receive'){
        chat_log.innerHTML += ('<p class="receive"> [Sender] ' + message + '</p>');
    }
}

// Focus al input text
document.querySelector('#chat-message-input').focus();

// On Enter pressed, the WebSocket is sent
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

// Al hacer click en el botón de enviar el websocket se envía
document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    websocket.send(JSON.stringify({
        'type':'chat_message',
        'message': message,
    }));
    console.log('WebSocket sent!');
    add_message('send', message);
    messageInputDom.value = '';
};