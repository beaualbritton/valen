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
console.log(root.oid)
</script>

<main class="bg-elevated border border-main rounded-lg overflow-hidden">
  {#if root.type === "blob" && lastRoot}
    {@render table(lastRoot)}
  {:else}
    {@render table(root)}
  {/if}
</main>

{#snippet table(root: any)}
<table class="w-2xl">
  <tbody class="w-xl divide-y">
    {#each root.entries as entry}
      <tr class="hover:bg-surface transition-colors duration-150">
        <td class="px-4 py-3">
          <a onclick={() => handleRefetch(entry.oid)} class="hover:text-green hover:underline">{entry.name}</a>
        </td>
        <td class="px-4 py-3 text-muted text-sm">
          {#if entryMap[entry.oid]}
            <div class="flex flex-row gap-1 items-center justify-center">
              <span class="text-main">{entryMap[entry.oid].response.commits.author}</span>
              <span>{entryMap[entry.oid].response.commits.message}</span>
              <span class="text-xs">{new Date(entryMap[entry.oid].response.commits.time * 1000).toLocaleDateString()}</span>
            </div>
          {:else}
            <span class="text-yellow">Loading…</span>
          {/if}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
{/snippet}
