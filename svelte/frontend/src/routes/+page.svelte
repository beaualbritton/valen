<script lang="ts">
let { data } = $props();

const user = data.user;
const userStatus = data.status;
console.log(data)
console.log(user)
console.log(userStatus)
</script>

<main class = "flex flex-col items-center justify-center min-h-screen">
  {#if userStatus}
    {@render dashboard(user)}
  {:else}
    {@render home()}
  {/if}
</main>

{#snippet home()}
  <h1 class = "text-9xl font-semibold">
    valen
  </h1>

  <h2 class = "text-lg">
    version control for everyone
  </h2>
{/snippet}

{#snippet dashboard(username: string)}
  <h1 class = "text-9xl font-semibold">
    dashboard
  </h1>

  <h2 class = "text-lg">
    hello, {username}
  </h2>
{/snippet}
