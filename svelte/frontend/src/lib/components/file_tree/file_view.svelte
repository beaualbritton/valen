<script lang="ts">
import { HighlightAuto } from "svelte-highlight";
import "$lib/styles/everforest-dark.css"
let { blob, toggle, handleToggle, commitHead = $bindable()} : { blob: any, toggle:boolean, handleToggle(): void, commitHead: any}= $props()
let code = blob.entries.split("\n").join("\n");
</script>

<svelte:head>
  {@html code}
</svelte:head>

{#if toggle}
  <div class="fixed inset-0 flex items-center justify-center bg-main/50 z-50 animate-fade-in p-4 w-full h-screen mt-4">
    <div class="flex flex-row bg-surface rounded-xl shadow-xl w-6xl overflow-y-auto border-white/20 border-2">
      <section class="w-full bg-elevated border border-main rounded-lg overflow-hidden">
        <div class = "h-16">
        <table class="w-full">
          <thead class="bg-surface h-16">
            <tr>
              <th class="px-4 py-4 text-left font-medium text-yellow texl-xl"> <span class ="nf nf-seti-git text-red text-lg flex-shrink-0"></span> {commitHead.author}:</th>
              <th class="px-4 py-4 text-left font-medium">
                {#if commitHead}
                  <div class="grid grid-cols-6 gap-2 items-center">
                    <span class="col-span-4 text-main italic truncate whitespace-nowrap overflow-hidden text-ellipsis">
                      {commitHead.message.split('\n')[0]}
                    </span>

                    <span class="text-md text-blue whitespace-nowrap hover:underline">
                      <span class="nf nf-cod-diff"></span> {commitHead.oid.substring(0,6)}
                    </span>
                    <button onclick={handleToggle} class ="ml-24 text-red hover:brightness-110 focus:brightness-90 transition-colors"aria-label="Close">
                      <span class = "nf nf-fa-close text-xl"></span>
                    </button>
                  </div>
                {:else}
                  <span class="text-yellow">Loading commit info…</span>
                {/if}
            </th>
            </tr>
          </thead>
        </table>
        </div>
        <div class="max-h-112 overflow-auto">
          <HighlightAuto {code} />
        </div>
      </section>
    </div>
  </div>
{/if}
