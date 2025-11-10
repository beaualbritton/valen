<script lang="ts">
let { commits, handleRefetch = $bindable()} : {commits: any, handleRefetch: (objectId: string) => void} = $props()
</script>

<main class = "border-black/80 border-2 rounded-lg h-64 overflow-scroll">
  <table>
    <thead>
      <tr><th>commits</th></tr>
    </thead>
    <tbody>
        {#each commits as commit}
          <tr>
            <td><a onclick={() => handleRefetch(commit.oid)} class="hover:underline">{commit?.author}: {commit?.message} </a></td>
            <td>@ {new Date(commit?.time * 1000).toLocaleDateString()}</td>
          </tr>
        {/each}
    </tbody>
  </table>
</main>

