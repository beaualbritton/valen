<script lang="ts">
import FileTree from "$lib/components/file_tree/file_tree.svelte";
import CommitList from "$lib/components/file_tree/commit_list.svelte";
import BranchList from "$lib/components/file_tree/branch_list.svelte";
import FileView from "$lib/components/file_tree/file_view.svelte";
let {data} = $props()
let repository = $state(data.repoData)
let user = $state(data.username)
let repoName = $state(data.repoName)
let root = $derived(repository.response.object)
let commits = $state(data.commits.response.commits)
let branches = $state(data.branches.response.branches)
let defaultBranch = $state(data.default.response.branches)
let blob = $state(false)
$inspect(branches)
$inspect(defaultBranch)

async function refetch(objectId : string) 
{
  // Calling internal server function with this fetch, see ./refetch/+server.ts 
  // Basically wraps refetch functionality on the server, instead of refreshing on the client.
  const query = `?oid=${encodeURIComponent(objectId)}`;
  const refetchResponse = await fetch(`/${user}/${repoName}/refetch${query}`);
  repository = await refetchResponse.json();

}
async function getLatestFromObject(objectId : string) 
{
  // Calling internal server function with this fetch, see ./latest/+server.ts 
  const query = `?oid=${encodeURIComponent(objectId)}`;
  const latestResponse = await fetch(`/${user}/${repoName}/latest${query}`);
  const latest = await latestResponse.json();
  console.log(latest)
  return latest;
}
</script>

<main>
  <div class = "min-h-screen flex flex-row items-center justify-center">
    <div class = "flex-col w-2/3">
      {#if root.type ==="blob"}
        <FileView blob={root}/>
      {/if}
      <FileTree root={root} handleRefetch={refetch} getLatest={getLatestFromObject} />
    </div>
    <div class = "w-1/3 flex flex-col">
      <CommitList commits={commits} handleRefetch={refetch}/>
      <BranchList branches={branches} defaultBranch={defaultBranch} handleRefetch={refetch}/>
    </div>
  </div>
 </main>
