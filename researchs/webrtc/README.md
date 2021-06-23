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

Steps to get Peer Connection working:
- First, on each side, create a peer connection.
- Create an event handler for "icecandidate" event, wich will add the opposite candidate on each peer to their candidate list.
- We need to create and "ontrack" handler wich will proccess the remote stream tracks received from the other peer.
- Also, its needed to send the tracks from the local peer to the remote peer using the method getTracks() to get all of them and for each track use addTrack(track, localStream) to set the tracks that the local peer need to send to the other.
- Finally, the local side need to create an offer, set its local description and send it to the remote peer, this peer will set its remote description and create an answer to that offer wich will be used to set it local description and, also, will be used by the local peer to set its remote description. Once all descriptions set, this peers will exchange ICE Candidates, add them to their lists, and start the RTC connection.

## MediaStream API (also known as getUserMedia API)
This API represents synchronized streams of media. For example, a stream taken from camenra and microphone input has synchronized video and audio tracks.