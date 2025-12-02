<script lang="ts">
let { commits, handleRefetch = $bindable()} : {commits: any, handleRefetch: (objectId: string) => void} = $props()
</script>

<div class="w-sm bg-elevated border border-main rounded-lg p-4 ">
  <h3 class="text-lg font-semibold text-green mb-3"><span class ="nf nf-seti-git text-red text-lg"></span> Commits</h3>
  <div class="space-y-3 h-96 overflow-scroll">
    {#each commits as commit}
      <button onclick={() => handleRefetch(commit.oid)} class="w-full text-left p-3 rounded bg-surface border border-main transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90">
        <div class="text-main font-medium mb-1">{commit.message}</div>
        <div class="text-muted text-sm">
          {commit.author} · {new Date(commit.time * 1000).toLocaleDateString()}
        </div>
      </button>
    {/each}
  </div>
</div>
