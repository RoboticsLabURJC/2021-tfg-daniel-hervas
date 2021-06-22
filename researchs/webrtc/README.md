# WebRTC
WebRTC apps do several things:
- Get streaming audio, video, or other data.
- Get network information, such as IP addresses and ports, and exchange it with other WebRTC clients (peers) to enable connection.
- Coordinate signaling comunication to report errors and initiate or close sessions.
- Exchange information about media and client capability, such as resolutiom and codecs.
- Communicate streaming audio, video or data.

WebRTC implements the following APIs:
- MediaStream gets access too daya streams, such as from the user's camera and microphone.
- RTCPeerConnection enables audio or video calling with facilities for encryption and bandwidth management.
- RTCDataChannel enables peer-to-peer communication of generic data.

## MediaStream API (also known as getUserMedia API)
This API represents synchronized streams of media. For example, a stream taken from camenra and microphone input has synchronized video and audio tracks.