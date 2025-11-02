<script lang="ts">
let {data} = $props()
let repository = $state(data.repoData)
let user = $state(data.username)
let repoName = $state(data.repoName)
let root = $derived(repository.response.object)

async function refetch(objectId : string) {

  const query = `?oid=${encodeURIComponent(objectId)}`;
  const res = await fetch(`/${user}/${repoName}/refetch${query}`);
  repository = await res.json();
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
        <li><a on:click={() => refetch(entry.oid)} class="underline">{entry.name}</a></li>
      </ul>
    {/each}
  {/if}
</main>
