<script>
  import { username, user } from '../user';

  function signout() {
    user.leave();
    username.set('');
  }
</script>

<header>
<h1>🔫💬</h1>
  {#if $username}
    <div class="user-bio">
      
      <span>Hello <strong>{$username}</strong></span>
      <img src={`https://api.dicebear.com/8.x/pixel-art/svg?seed=${$username}`} alt="avatar" /> 
    </div>

    <button class="signout-button" on:click={signout}>Sign Out</button>

    {:else}

      <h3>Gun.js Chat</h3>
  {/if}
</header>