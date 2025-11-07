<script lang="ts">
import FileView from "./file_view.svelte";
let { root, handleRefetch, getLatest = $bindable()} : {root: any, handleRefetch: (objectId: string) => void, getLatest: any} = $props()

// TypeScript utility sugar. Basically a Map object with types
// https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type
let entryMap = $state<Record <string, any>>({});
let lastRoot: any;

// Effects run whenever a state is updated. In this case, whenever root changes (handled by parent. FileTree just observes)
// https://svelte.dev/docs/svelte/$effect
function setLastRoot(root: any)
{
  lastRoot = root;
}

$effect(() => {
    if (!root?.entries || root.type == "blob") return;
    setLastRoot(root);
    //Asynchronous function that maps the latest info with new entries upon FileTree navigation
    (async () =>
    {
      const map: Record<string, any> = {};
      for (const entry of root.entries)
      {
        try
        {
          map[entry.oid] = await getLatest(entry.oid);
        }
        catch (err)
        {
          console.error('Error fetching latest for', entry.oid, err);
        }
      }
      entryMap = map;
    })
    //Might seem weird but this calls the previous async function
    //"Immediately Invoked Function Expression." Basically crackhead javascript https://developer.mozilla.org/en-US/docs/Glossary/IIFE
    ();
});
</script>

<main class = "border-black/80 border-2 rounded-lg w-1/2">
  {#if root.type === "blob" && lastRoot}
    {@render table(lastRoot)}
  {:else}
    {@render table(root)}
  {/if}
</main>

{#snippet table(root: any)}
<table>
  <tbody>
    {#each root.entries as entry}
      <tr>
        <td>
          <a onclick={() => handleRefetch(entry.oid)} class="hover:underline">{entry.name}</a>
        </td>
        <td>
          {#if entryMap[entry.oid]}
            <a class="justify-center hover:underline">
              {entryMap[entry.oid].response.commits.author}: 
              {entryMap[entry.oid].response.commits.message} @ 
              {new Date(entryMap[entry.oid].response.commits.time * 1000).toLocaleDateString()}
            </a>
          {:else}
            Loading…
          {/if}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
{/snippet}
