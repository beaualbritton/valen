<script lang="ts">
let { repoList, user = $bindable()} : {repoList: string[], user: string} = $props()
</script>

<main>
  {#each repoList as repo}
    <table>
      <tbody>
        <tr>
          <td> <a href="/{repo}" class="hover:underline">{repo}</a></td>
        </tr>
      </tbody>
    </table>
  {/each}
</main>
