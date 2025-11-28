<script lang="ts">
import CreateRepoButton from '$lib/components/dashboard/CreateButton.svelte';
import CreateRepoForm from '$lib/components/dashboard/CreateForm.svelte';
let { data } = $props();
const user = data.user;
const userStatus = data.status;

let toggle: boolean = $state(false);
const handleToggle = () => toggle = !toggle;
</script>

<main class = "flex flex-col items-center justify-center min-h-screen">
  {#if userStatus}
    {@render dashboard(user)}
  {:else}
    {@render home()}
  {/if}
</main>

{#snippet home()}
  <h1 class = "text-9xl font-semibold text-green">
    valen
  </h1>

  <h2 class = "text-lg text-yellow">
    version control for everyone
  </h2>
{/snippet}

{#snippet dashboard(username: string)}
  <h1 class = "text-9xl font-semibold text-green">
    dashboard
  </h1>

  <h2 class = "text-lg text-yellow mb-4">
    hello, {username}
  </h2>

  <CreateRepoButton toggle={handleToggle} title={"create new repo"}/> 

  <CreateRepoForm toggle={toggle} handleToggle={handleToggle} user={username}/>
{/snippet}
