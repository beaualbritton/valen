<script lang="ts">
import FileView from "./file_view.svelte";
let { root, handleRefetch, getLatest, commitHead= $bindable()} : {root: any, handleRefetch: (objectId: string) => void, getLatest: any, commitHead: any} = $props()

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
<table class="w-3xl">
  <thead class="bg-surface h-16">
    <tr>

    <th class="px-4 py-4 text-left font-medium text-yellow text-md">
      <div class="flex items-center gap-2">
        <span class="nf nf-seti-git text-red text-lg flex-shrink-0"></span>
        <span class="truncate block">{commitHead.author}:</span>
      </div>
    </th>
      <th class="px-4 py-4 text-left font-medium">
        {#if commitHead}
          <div class="grid grid-cols-6 gap-2 items-center">
            <span class="col-span-4 text-main italic text-md truncate whitespace-nowrap overflow-hidden text-ellipsis">
              {commitHead.message.split('\n')[0]}
            </span>

            <span class="text-xs text-blue whitespace-nowrap hover:underline">
              <span class="nf nf-cod-diff"></span> {commitHead.oid.substring(0,6)}
            </span>
            <span class="text-xs text-muted whitespace-nowrap">
              {new Date(commitHead.time * 1000).toLocaleDateString()}
            </span>
          </div>
        {:else}
          <span class="text-yellow">Loading commit info…</span>
        {/if}
      </th>
    </tr>
  </thead>
  <tbody class="w-xl divide-y divide-black/20">
    {#each root.entries as entry}
      <tr class="hover:bg-surface transition-colors duration-150">
        <td class="px-4 py-3">
          <div class="flex items-start gap-2">
            {#if entry.type === "tree"}
              <span class="nf nf-fa-folder text-blue flex-shrink-0"></span>
            {:else}
              <span class="nf nf-fa-file text-yellow flex-shrink-0"></span>
            {/if}
            <a onclick={() => handleRefetch(entry.oid)} class="text-green font-bold hover:underline break-words truncate block">
              {entry.name}
            </a>
          </div>
        </td>
        <td class="px-4 py-3 text-muted text-sm">
          {#if entryMap[entry.oid]}
            <div class="grid grid-cols-6 gap-2 items-center">
              <span class="col-span-4 truncate italic overflow-hidden text-ellipsis text-main">
                {entryMap[entry.oid].response.commits.message}
              </span>
              <span class="whitespace-nowrap overflow-hidden text-ellipsis">
                {entryMap[entry.oid].response.commits.author}
              </span>
              <span class="text-xs whitespace-nowrap">
                {new Date(entryMap[entry.oid].response.commits.time * 1000).toLocaleDateString()}
              </span>
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
