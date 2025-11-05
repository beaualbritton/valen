<script lang="ts">
import FileTree from "$lib/components/file_tree/file_tree.svelte";
let {data} = $props()
let repository = $state(data.repoData)
let user = $state(data.username)
let repoName = $state(data.repoName)
let root = $derived(repository.response.object)

async function refetch(objectId : string) 
{
  // Calling internal server function with this fetch, see ./refetch/+server.ts 
  // Basically wraps refetch functionality on the server, instead of refreshing on the client.
  const query = `?oid=${encodeURIComponent(objectId)}`;
  const res = await fetch(`/${user}/${repoName}/refetch${query}`);
  repository = await res.json();
}
</script>

<main>
  <div class = "min-h-screen flex items-center justify-center">
      <FileTree root={root} handleRefetch={refetch}/>
  </div>
 </main>
