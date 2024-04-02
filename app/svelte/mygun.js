import Gun from "gun/gun";
import "gun/lib/webrtc";

let peers;

if (false) {
  peers = ["http://localhost:8765/gun"];
} else {
  peers = [
    // Community relay peers: https://github.com/amark/gun/wiki/volunteer.dht
    "https://gun-manhattan.herokuapp.com/gun",
   // "https://relay.129.153.59.37.nip.io/gun",
   // "https://relay.peer.ooo/gun",
   // "https://peer.wallie.io/gun",
   // "www-dweb-gun.dev.archive.org/gun",
   // "https://gundb-relay-mlccl.ondigitalocean.app/gun",
   // "https://plankton-app-6qfp3.ondigitalocean.app/"
  ];
}

const gun = new Gun({
  peers,
});

// attaching gun to window for testing purposes
window.gun = gun;

export { gun };