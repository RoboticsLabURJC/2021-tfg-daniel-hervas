'use strict';


let stream;
let localStream;
let pc1;
let pc2;

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

let iceCandidates = [];

let startButton = document.querySelector('#startButton');

startButton.addEventListener('click', startStream);

async function startStream(){
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

    var configuration = {
        "iceServers": [{ "urls": "stun:stun.1.google.com:19302" }]
    };

    // Creo el peer para cada usuario
    pc1 = new RTCPeerConnection(configuration);
    pc2 = new RTCPeerConnection(configuration);
    console.log('Created RTC Peers');

    // Handlers para cuando hay candidatos
    pc1.addEventListener('icecandidate', e => onIceCandidate(pc1, e));
    pc2.addEventListener('icecandidate', e => onIceCandidate(pc2, e));
    console.log("Added candidates handlers created.");

    // Establecer el vídeo local en el remoto
    pc2.ontrack = gotRemoteStream;

    // Notificar si el estado remoto cambia
    pc2.oniceconnectionstatechange = () => console.log('PC2 ice state ' + pc2.iceConnectionState);
    console.log("localStream: " + localStream);

    // Añadir tracks a la PeerConnection
    // console.log(`Streamed tracks added ${localStream.getTracks()[0].label}`);
    localStream.getTracks().forEach(track => pc1.addTrack(track, localStream));

    // Crear oferta SDP desde el extremo local y respuesta desde el extremo
    // IMPORTANTE: Para establecer la conexión, es necesario que ambos
    // extremos tengan establecida su descripción.
    try{
        const offer = await pc1.createOffer(offerOptions)
        // Establecer la descripcion del extremo local
        try{
            await pc1.setLocalDescription(offer);
            console.log('Pc1 Local description set');
        }catch(error){
            console.log(`Failed to set local description: ${error}`);
        }
        // Set remote connection
        setRemoteConnection(offer);
    }catch(error){
        console.log(`Failed to send SDP offer: ${error}`);
    }
}


async function setRemoteConnection(offer){
    try {
        await pc2.setRemoteDescription(offer);
        console.log(`Pc2 remote Description set`);
      } catch (error) {
        console.log(`Failed to set session description: ${error.toString()}`);
      }
    
      try {
        const answer = await pc2.createAnswer();
    
        try {
          await pc2.setLocalDescription(answer);
          console.log("Pc2 local description created.");
        } catch (error) {
          console.log(`Failed to set session description: ${error.toString()}`);
        }
    
        try {
          await pc1.setRemoteDescription(answer);
          console.log("Pc1 remote description set.")
        } catch (error) {
          console.log(`Failed to set session description: ${error.toString()}`);
        }
      } catch (error) {
        console.log(`Failed to create session description: ${error.toString()}`);
      }
}

function getOtherPc(pc){
    return (pc === pc1) ? pc2 : pc1;
}

function getName(pc){
    return (pc === pc1) ? 'pc1' : 'pc2';
}

async function onIceCandidate(pc, e){
    try{
        if(e.candidate){
            console.log(`${getName(pc)} new ${e.candidate}`);
            await getOtherPc(pc).addIceCandidate(e.candidate);
            console.log(getName(getOtherPc(pc)));
      
            iceCandidates.push(e.candidate);
        }
    
        let strList = "";
        iceCandidates.forEach(element => {
            strList += element + '\n';
        });
        console.log(strList);
    }catch(error){
        console.log(`${pc} failed to add ICE Candidate: ${error}`);
    }   
}

function gotRemoteStream(e){
    console.log('Remote stream: ', e);
    // Establecer el vídeo del remoto
    remoteVideo.srcObject = e.streams[0];
    console.log('pc2 received remote stream');
}