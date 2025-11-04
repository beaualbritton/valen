<script lang="ts">

let { root, handleRefetch= $bindable()} : {root: any, handleRefetch: (objectId: string) => void; } = $props()

</script>

<main class = "border-black/80 border-2 rounded-lg w-1/2">
  {#if root.type === "blob"}
    <pre>
      {#each root.entries.split("\n") as entry}
        {entry}
      {/each}
    </pre>
  {:else}
    <table>
      <tbody>
        {#each root.entries as entry}
          <tr>
            <!-- TODO: reflect navifation as file system--> 
            <td>
              <a onclick={() => handleRefetch(entry.oid)} class="hover:underline" href="">{entry.name}</a>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</main>
