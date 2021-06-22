'use strict';

let token = new Date().getTime() + Math.random();
console.log('token: ',token);

websocket.onmessage = function(event){
    let message_data = JSON.parse(event.data);
    console.log('WebSocket received: ', message_data);

    // If the content type from the websocket is chat_message,
    // the text field is appended to the chat box
    if(message_data['type'] == 'chat_message'){
        if(Number(token) !== Number(message_data['token'])){
            console.log('Escribir mensaje');
            add_message('receive', message_data['message']);
        }
    }

};

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
        'token':token,
        'message': message,
    }));
    console.log('WebSocket sent!');
    add_message('send', message);
    messageInputDom.value = '';
};