<script lang="ts">
let { repoList, user = $bindable()} : {repoList: string[], user: string} = $props()
console.log(repoList)
</script>

<main class="bg-elevated border border-main rounded-lg p-4" >
  <div class="space-y-3">
    {#if repoList.length > 0}
      {#each repoList as repo}
        <a class="w-full p-3 rounded bg-surface border border-main transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90 flex items-center gap-2 " href="/{repo}">
          <div class="flex-col">
            <div class="text-main font-medium">{repo}</div>
            <!-- TODO: descriptions for repos. maybe languages -->
            <div class="text-muted text-sm">Description</div>
          </div>
        </a>
      {/each}
    {:else}
      <div class="p-6 text-center">
        <p class="text-muted">No repositories yet</p>
      </div>
    {/if}
  </div>
</main>
