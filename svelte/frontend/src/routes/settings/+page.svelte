<script lang="ts">
let { data } = $props<{ response: any; user: any}>();
import { createToken } from "$lib/api/tokens";
console.log(data)
console.log(data.response)
console.log(data.user)
let tokenResponse: any = $state();
async function requestToken()
{
  const name: string = "new-token"
  const expiration: Date = new Date(Date.now() + 24 * 60 * 60 * 1000);

  const {response} = await createToken(name, expiration);
  tokenResponse = response
}
</script>

<main>
settings

  <button onclick={requestToken}>
    create token?
  </button>
  {#if tokenResponse}
    <p>tokenResponse</p>
  {/if}
</main>
