<script>
	export let message;
	export let sender;
  
	const messageClass = message.who === sender ? 'chat-start' : 'chat-end';
	const is_human = message.who === 'llm' ? false : true
	console.log(message, sender, message.who)
  
	const avatar_human = `https://api.dicebear.com/8.x/pixel-art/svg?seed=${message.who}`
	const avatar_not_human = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/HAL9000.svg/1920px-HAL9000.svg.png'
	const ts = new Date(message.when);
  </script>
  
  <div class={`chat ${messageClass}`}>
	<div class="chat-image avatar">
		<div class="w-10 rounded-full">
		  <img alt="Tailwind CSS chat bubble component" src={is_human? avatar_human: avatar_not_human} />
		</div>
	  </div>
	  <div class="chat-header">
		{message.who}
		<time class="text-xs opacity-50">{ts.toLocaleTimeString()}</time>
	  </div>
	  <div class="chat-bubble whitespace-pre-line">{message.what}</div>

	</div>


  

	<style global lang="postcss">
		@tailwind base;
		@tailwind components;
		@tailwind utilities;
	</style>
