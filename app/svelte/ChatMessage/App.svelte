<script>
	export let message;
	export let sender;
  
	const messageClass = message.who === sender ? 'chat-start' : 'chat-end';
	console.log(message, sender, message.who)
  
	const avatar = `https://api.dicebear.com/8.x/pixel-art/svg?seed=${message.who}`
  
	const ts = new Date(message.when);
  </script>
  
  <div class={`chat ${messageClass}`}>
	<div class="chat-image avatar">
		<div class="w-10 rounded-full">
		  <img alt="Tailwind CSS chat bubble component" src={avatar} />
		</div>
	  </div>
	  <div class="chat-header">
		{message.who}
		<time class="text-xs opacity-50">{ts.toLocaleTimeString()}</time>
	  </div>
	  <div class="chat-bubble">{message.what}</div>

	</div>


  

	<style global lang="postcss">
		@tailwind base;
		@tailwind components;
		@tailwind utilities;
	</style>
