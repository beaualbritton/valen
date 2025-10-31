<script lang="ts">
import { fetchRepository } from "$lib/repository";
let {data} = $props()
let repository = $state(data.repoData)
let user = $state(data.username)
let repoName = $state(data.repoName)
let root = $derived(repository.response.object)

async function fetch(objectId: string)
{
  let response = fetchRepository(user, repoName, objectId)
  repository = await response
  console.log(response)
}
</script>

<main>
  {#if root.type === "blob"}
    <pre>
      {#each root.entries.split("\n") as entry}
        {entry}
      {/each}
    </pre>
  {:else}
    {#each root.entries as entry}
      <ul>
        <li><a on:click={() => fetch(entry.oid)} class="underline">{entry.name}</a></li>
      </ul>
    {/each}
  {/if}
</main>
