function python_send_message(message){
 // Send POST request to Flask backend
 var xhr = new XMLHttpRequest();
 xhr.open("POST", "/send_message", true);
 xhr.setRequestHeader("Content-Type", "application/json");
 xhr.onreadystatechange = function() {
     if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
         console.log("message send");
     }
 };
 var data = JSON.stringify({"message": message});
 xhr.send(data);
return 
}
export {python_send_message};