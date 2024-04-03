<script>
	import Login from '../Login/App.svelte'
	import ChatMessage from '../ChatMessage/App.svelte'
	import { onMount } from 'svelte';
	import { username, user } from '../user';
	import debounce from 'lodash.debounce';
	import {gun} from '../mygun';
	import Gun from "gun/gun";
	import {python_send_message} from '../flask'

	const session_id =  document.data.session_id;
	const db = gun;
	const chat_room = `chat/${session_id}`

	let encrypt_key =  '#foo'; //Idea -> session_id
	let encrypt_message = false;

	let newMessage;
	let messages = [];
  
	let scrollBottom;
	let lastScrollTop;
	let canAutoScroll = true;
	let unreadMessages = false;

/* 	const eventSource = new EventSource('/events');

	eventSource.onmessage = function(event) {
		console.log('Message from server:', event);
	};

	eventSource.onerror = function(error) {
		console.error('EventSource failed:', error);
	}; */
  
	function autoScroll() {
	  setTimeout(() => scrollBottom?.scrollIntoView({ behavior: 'auto' }), 50);
	  unreadMessages = false;
	}
  
	function watchScroll(e) {
	  canAutoScroll = (e.target.scrollTop || Infinity) > lastScrollTop;
	  lastScrollTop = e.target.scrollTop;
	}
  
	$: debouncedWatchScroll = debounce(watchScroll, 1000);
  
	onMount(() => {
	  var match = {
		// lexical queries are kind of like a limited RegEx or Glob.
		'.': {
		  // property selector
		  '>': new Date(+new Date() - 1 * 1000 * 60 * 60 * 3).toISOString(), // find any indexed property larger ~3 hours ago
		},
		'-': 1, // filter in reverse
	  };
	  
	  // llm stream has to be assebled here
	  var llm_response = ''
	  // Get Messages
	  db.get(chat_room)
		.map(match)
		.once(async (data, id) => {
		  if (data) {
			console.log("TP 1")
			if (data.hasOwnProperty('stream')){

				const message_nr = llm_response===''? messages.length: messages.length-1
				console.log(message_nr)
				llm_response += (await decrypt(data.what)) + ''
				var message = {
					// transform the data
					who: data.who, // a user might lie who they are! So let the user system detect whose data it is.
					what: llm_response, // force decrypt as text.
					when: Gun.state.is(data, 'what'), // get the internal timestamp for the what property.
				};
				if (message_nr === message.length){
					messages = [...messages.slice(-100), message].sort((a, b) => a.when - b.when);
				}else{
					messages[message_nr]=message	
				}
				

			}else{
				console.log("TP 2")
				llm_response= ''
				var message = {
					// transform the data
					who: await db.user(data).get('alias'), // a user might lie who they are! So let the user system detect whose data it is.
					what: (await decrypt(data.what)) + '', // force decrypt as text.
					when: Gun.state.is(data, 'what'), // get the internal timestamp for the what property.
				};
  
				if (message.what) {
            		messages = [...messages.slice(-100), message].sort((a, b) => a.when - b.when);
            		if (canAutoScroll) {
              			autoScroll();
            		} else {
              			unreadMessages = true;
            		}
				}
			}
		  }
		});
	});
	async function encrypt(message){
		if (encrypt_message){
			return await SEA.encrypt(message, encrypt_key);
		}else{return message}
	}
	async function decrypt(message){
		if(encrypt_message){
			return (await SEA.decrypt(message, encrypt_key)) + ''
		}else{return message}
	}
	async function python_stream_llm_response(stream_id){
	
    const index = new Date().toISOString();
	var doc = '';
	const eventSource = new EventSource(`/stream_message/${stream_id}`);
	eventSource.onerror = function(error) {
		console.error('EventSource failed:', error);
	};
	

	eventSource.onmessage = async function(event) {
		const message = JSON.parse(event.data);
		if (message.done === true){
			eventSource.close()
		}else{
			const secret = await encrypt(message.message.content);
			
			const index = new Date().toISOString();
			db.get(chat_room).get(index).put({ 
				what: secret,
				who: 'llm',
				stream: true
			})
			
			 // Assuming message is sent as JSON
		}
	};
	async function handleMessage(){
		const secret = await encrypt(doc);
			console.log("response = ", secret)
			const index = new Date().toISOString();
			db.get(chat_room).get(index).put({ 
				what: secret,
				who: 'llm',
				stream: true
			})
	}
	// Process messages from the queue at a controlled rate
	const processMessages = () => {
    if (messageQueue.length > 0) {
        const message = messageQueue.shift();
        handleMessage(message);
    }
    // Adjust the delay time (in milliseconds) to control the rate
    setTimeout(processMessages, 100); // Process one message every 100 milliseconds
};
}
  
	async function sendMessage() {

		python_send_message(session_id, newMessage)
    		
	  	const secret = await encrypt(newMessage);
		  const msg= { 
				what: secret,
			}
	  	const message = user.get('all').set(msg);
		const index = new Date().toISOString();
		db.get(chat_room).get(index).put(message)	;
	  console.log("TP2")
	  newMessage = '';
	  canAutoScroll = true;
	  autoScroll();
	  python_stream_llm_response(session_id)
	}

	async function python_get_message(){
		fetch('/get_message')
        .then(response => response.json())
        .then(async data => {
			const secret = await encrypt(data.content)
			const msg= { 
				what: secret,
				who: 'llm'
			}
	  		const message = user.get('all').set(msg);
			const index = new Date().toISOString();
			db.get(chat_room).get(index).put(message)	
        })
        .catch(error => {
            console.error('Error:', error);
        })
	}
  </script>
  
  <div class="container">
	{#if $username}
	  <main on:scroll={debouncedWatchScroll}>
		{#each messages as message (message.when)}
		  <ChatMessage {message} sender={$username} />
		{/each}
  
		<div class="dummy" bind:this={scrollBottom} />
	  </main>
  
	  <form class="bottom-form" on:submit|preventDefault={sendMessage}>
		<input type="text" placeholder="Type a message..." bind:value={newMessage} maxlength="100" style="height: 50px; font-size: 16px;" />
		<!-- Adjusted input field height and font size -->
  
		<button type="submit" disabled={!newMessage}>💥</button>
	  </form>
  
	  {#if !canAutoScroll}
		<div class="scroll-button">
		  <button on:click={autoScroll} class:red={unreadMessages}>
			{#if unreadMessages}
			  💬
			{/if}
			👇
		  </button>
		</div>
	  {/if}
	{:else}
	  <main>
		<Login />
	  </main>
	{/if}
  </div>
  
  <style>
	.container {
	  display: flex;
	  flex-direction: column;
	  height: 100vh;
	  overflow: hidden; /* To prevent form from being pushed outside container */
	}
  
	main {
	  flex-grow: 1;
	  overflow-y: auto; /* Enable scrolling */
	  padding-bottom: 2rem; /* Add some space at the bottom for the form */
	}
  
	form.bottom-form {
	  display: flex;
	  align-items: center;
	  justify-content: space-between;
	  padding: 1rem;
	  background-color: #f0f0f0;
	}
  
	input[type="text"] {
	  flex-grow: 1;
	  margin-right: 1rem; /* Add some space between the input field and the button */
	}
  
	button[type="submit"] {
	  width: 40px;
	  height: 40px;
	  font-size: 20px;
	}
  </style>
  