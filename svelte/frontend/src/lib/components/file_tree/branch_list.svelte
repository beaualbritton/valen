<script lang="ts">
let { branches, defaultBranch, handleRefetch = $bindable()} : {branches: any, defaultBranch: any, handleRefetch: (objectId: string) => void} = $props()
</script>

<div class="w-sm bg-elevated border border-main rounded-lg p-4">
  <h3 class="text-lg font-semibold text-green mb-3">Branches</h3>
  
  <div class="space-y-2">
    <button 
      onclick={() => handleRefetch(defaultBranch.oid)} class="w-full text-left px-3 py-2 rounded bg-surface border border-main text-main font-medium transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90">
      <span class="text-green">★</span> {defaultBranch.branch} 
      <span class="text-muted text-sm ml-2">(default)</span>
    </button>

    {#each branches as branch}
      <button 
        onclick={() => handleRefetch(branch.oid)} class="w-full text-left px-3 py-2 rounded bg-surface border border-main text-main transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90">
        {branch.branch}
      </button>
    {/each}
  </div>
</div>
