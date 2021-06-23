'use strict';

let stream;
let localStream;
let localPeer;
let remotePeer;

const constraints = {
    video: {
    mediaSource: "screen", // whole screen sharing
    //mediaSource: "window", // choose a window to share
    //mediaSource: "application", // choose a window to share
    width: {max: '1920'},
    height: {max: '1080'},
    frameRate: {max: '10'}
    }
};

const offerOptions = {
    OfferToReceiveAudio: 1,
    OfferToReceiveVideo: 1
};

var configuration = {
    "iceServers": [{ "urls": "stun:stun.1.google.com:19302" }]
};

let iceCandidates = [];

let startButton = document.querySelector('#startButton');

startButton.addEventListener('click', checkUsers);

function checkUsers() {
    websocket.send(
      JSON.stringify({
        type: "check-users",
      })
    );
  }

// Empezar el streaming local:
//   1. Desactivar el botón de start, localVideo.play(),
//      obtener el media stream, establecer localVideo.srcObject = stream y
//      dar valor a la variable localStream con el stream que hemos obtenido.
//   2. Crear la instancia de la RTCPeerConnection
//   3. Crear el handler del evento icecandidate
//   4. Añadir los media tracks del localStream para que sean enviadas
//      al remote peer
//   5. Crear la oferta de candidato en el extremo local
//   6. Crear la descripción local de localPeer
async function startLocalStream(){  
    // Desactivar el botón de start
    startButton.disabled = true;

    // Para que no solo se muestre un frame de la pantalla
    localVideo.play();

    // Obtener el stream del usuario
    //stream = await navigator.mediaDevices.getUserMedia(constraints)   // Cámara
    stream = await navigator.mediaDevices.getDisplayMedia(constraints)  // Pantalla

    // Mostrar el video
    localVideo.srcObject = stream;

    // Establecer cual es el localStream
    localStream = stream;

    // Crear instancia de RTCPeerConnection
    localPeer = new RTCPeerConnection(configuration);

    // Send candidate to the remote peer
    localPeer.addEventListener('icecandidate', event => onIceCandidate(localPeer, event));

    // Añadir los media tracks que genera el localStream a
    // las tracks de localPeer para enviarlas al remote peer
    localStream.getTracks().forEach(track => localPeer.addTrack(track, localStream));
    console.log('Adding tracks');

    // Crear oferta
    localPeer.createOffer(offerOptions);

    // Establecer la descripcion de localPeer
    localPeer.addEventListener('negotiationneeded', addLocalDescription(localPeer));
}

// Cuando recibo un socket del tipo offer:
// 1. Creo la instancia de la conexión RTC del extemo remoto
// 2. Creo el hadler para el evento icecandidate
// 3. Handler para recibir los mediatracks
// 4. Notifico si el estado del remotePeer cambia
// 5. Establezco la descripcion remota del extremo remoto
// 6. Crear respuesta y establecer la descripcion local del extremo remoto
// 7. Enviar un websocket con la respuesta al otro peer
async function startRemoteStream(offer){
    // Creo la instancia de la conexión remota
    remotePeer = new RTCPeerConnection(configuration);
    console.log('RTC Remote Peer conection created');

    // Handler para el evento icecandidate
    // Send candidate to the remote peer
    remotePeer.addEventListener('icecandidate', event => onIceCandidate(remotePeer, event));

    // Recibir los media tracks del extremo local
    remotePeer.ontrack = gotRemoteStream;

    // Notificar si el estado remoto cambia
    remotePeer.oniceconnectionstatechange = () => console.log('Remote ice state ' + remotePeer.iceConnectionState);

    // Set remote description
    try {
        remotePeer.setRemoteDescription(offer);
        console.log('Remote description set');
    } catch (error) {
        console.log(`Set remote description error: ${error}`);
    }

    try {
        // Create answer
        const answer = await remotePeer.createAnswer();
        // Set local description of remote peer
        remotePeer.setLocalDescription(answer);
        // Signal localStream peer with the answer
        signalRemotePeer(JSON.stringify({
            'type':'answer',
            'answer':answer
        }));
    }catch(error){
        console.log(`Failed to create local session description ${error}`);
    }
    
    
}

function addIceCandidate(candidate) {
    //var candidate = new RTCIceCandidate(cand)
    if (localPeer === undefined) {
      remotePeer.addIceCandidate(candidate);
    } else {
      localPeer.addIceCandidate(candidate);
    }
    console.log('Candidate Added');
  }

async function setAnswerDescription(answer){
    try {
        localPeer.setRemoteDescription(answer);
        console.log("Local Peer remote description set");
    }catch(error){
        console.log(`Failed setting local peer remote description ${error}`);
    }
}

// Añadir los candidatos a la lista de candidatos
function onIceCandidate(peer, event){
    if(event.candidate != null && event.candidate != undefined){
        console.log(`onicecandidate event on ${peer}`);
        // Send the candidate to the other peer via WebSockets
        //signalRemotePeer(JSON.stringify({
        //     'type':'candidate',
        //     'candidate':event.candidate
        // }));
        websocket.send(JSON.stringify({
            'type':'candidate',
            'candidate':event.candidate
        }));
    }
}

async function addLocalDescription(peer) {
    try {
      const offer = await peer.createOffer(offerOptions);
      peer.setLocalDescription(offer);
      console.log(`${peer} local description set`);
      signalRemotePeer(JSON.stringify({
        'type':'offer',
        'offer':offer
    }));
    } catch(err) {
      console.log(`${peer} error setting local description`);
    }
}

function signalRemotePeer(data){
    websocket.send(data);
    console.log('Signaling remote peer...');
}

function gotRemoteStream(e){
    console.log('Got remote video: ', e.streams[0]);
    if (remoteVideo.srcObject !== e.streams[0]) {
        //rightVideo.play();
        remoteVideo.srcObject = e.streams[0];
        console.log('pc2 received remote stream');
    }
}