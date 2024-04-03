<script>
  import { username, user } from '../user';

  function signout() {
    user.leave();
    username.set('');
  }
</script>

<header>
  <h1>Pizza AI 🔫💬</h1>
  {#if $username}
    <div class="user-info">
      <div class="user-bio">
        <span>Hello <strong>{$username}</strong></span>
      </div>
      <div>
        <img src={`https://api.dicebear.com/8.x/pixel-art/svg?seed=${$username}`} alt="avatar" />
      </div>
    </div>
    <button class="signout-button" on:click={signout}>Sign Out</button>
  {:else}
    <h3>ollama & Gun.js chat</h3>
  {/if}
</header>

<style>
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    background-color: #f0f0f0;
    color: #333;
  }
  .user-info {
    display: flex; /* Display the username and avatar side by side */
    align-items: center; /* Vertically center the content */
  }
  .user-bio {
    margin-right: 1rem; /* Add some space between the username and the avatar */
  }
  img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
  }
</style>



<!-- <h1>🔫💬</h1>
  {#if $username}
    <div class="user-bio">
      
      <span>Hello <strong>{$username}</strong></span>
      <img src={`https://api.dicebear.com/8.x/pixel-art/svg?seed=${$username}`} alt="avatar" /> 
    </div>

    <button class="signout-button" on:click={signout}>Sign Out</button>

    {:else}

      <h3>Gun.js Chat</h3>
  {/if} -->