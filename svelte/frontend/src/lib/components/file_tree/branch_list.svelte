<script lang="ts">
let { branches, defaultBranch, handleRefetch = $bindable()} : {branches: any, defaultBranch: any, handleRefetch: (objectId: string) => void} = $props()
</script>


<main class = "border-black/80 border-2 rounded-lg ">
  <table>
    <thead>
      <tr><th>branches</th></tr>
    </thead>
    <tbody>
        <tr>
          <td><a onclick={() => handleRefetch(defaultBranch.oid)} class="hover:underline">default:{defaultBranch.branch}</a></td>
        </tr>
        {#each branches as branch}
          <tr>
            <td><a onclick={() => handleRefetch(branch.oid)} class="hover:underline">{branch.branch}</a></td>
          </tr>
        {/each}
    </tbody>
  </table>
</main>

