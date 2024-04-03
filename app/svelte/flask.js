
function python_send_message2(session_id,message){
 // Send POST request to Flask backend
 var xhr = new XMLHttpRequest();
 xhr.open("POST", "/send_message", true);
 xhr.setRequestHeader("Content-Type", "application/json");
 xhr.onreadystatechange = function() {
     if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
         console.log("message send");
     }
 };
 var data = JSON.stringify({"message": message,'session_id':session_id});
 xhr.send(data);
 xhr.response
return 
}
async function python_send_message(session_id, newMessage) {
    // Send message to Flask backend
    const response = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ session_id: session_id, message: newMessage })
    });

    // Extract stream ID from the response
    const { stream_id } = await response.json();

    // Return stream ID
    return stream_id;
}

export {python_send_message};