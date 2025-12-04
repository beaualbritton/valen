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
let currentUser = $state()
let commitOID = $state(root.oid)
let rootType = $derived(root.type)
let commitHead = $state(root)

let blobToggle = $state(false);
const handleBlobToggle = () => { blobToggle = !blobToggle}

if (data.currentUser.status)
{
  currentUser = data.currentUser.user.username
}

$effect(() =>
{
  if (rootType === "commit") 
  {
    if (commitOID !== root.oid) 
    {
      commitOID = root.oid;
    }
    commitHead = root;
  }
});

$effect(() => 
{
  if (rootType === "tree") 
  {
    getLatestFromObject(root.oid).then(result => 
    {
      commitHead = result.response.commits;
    });
  }
});

$effect(() =>  
{
  if (rootType === "blob")
  {
    getLatestFromObject(root.oid).then(result => 
    {
      commitHead = result.response.commits;
    });

    blobToggle = true;
  }
});

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
  const query = `?oid=${encodeURIComponent(objectId)}&fromCommitOID=${encodeURIComponent(commitOID)}`;
  const latestResponse = await fetch(`/${user}/${repoName}/latest${query}`);
  const latest = await latestResponse.json();
  return latest;
}
</script>

{#if blobToggle}
  {#key root.oid}
    <FileView blob={root} toggle={blobToggle} handleToggle={handleBlobToggle} commitHead={commitHead}/>
  {/key}
{/if}

<main class="bg-main min-h-screen pt-16 transition-all duration-500" class:blur-md={blobToggle}>
  <div class="min-h-screen flex flex-row items-start justify-center">
    <div class="flex flex-col gap-4 w-2/3 items-center justify-center min-h-screen">
      <div class = "w-3xl flex gap-4 flex-row justify-end">
        <button class="bg-surface border border-main text-green px-4 py-2 rounded font-medium transition-all duration-150 active:scale-95 active:brightness-90 hover:brightness-110">
          <span class = "nf nf-fa-cloud_download "></span> clone
        </button>
       {#if currentUser == user}
          <a class="bg-surface border border-main text-muted px-4 py-2 rounded font-medium transition-all duration-150 active:scale-95 active:brightness-90 hover:brightness-110" href ={`/${user}/${repoName}/settings`}> <span class="nf-fa-cog"></span> settings</a>
        {/if}
      </div>
      <FileTree root={root} handleRefetch={refetch} getLatest={getLatestFromObject} commitHead={commitHead}/>
    </div>

    <div class="flex flex-col gap-4 w-1/3 items-center justify-center min-h-screen">
      <CommitList commits={commits} handleRefetch={refetch}/>
      <BranchList branches={branches} defaultBranch={defaultBranch} handleRefetch={refetch}/>
    </div>
  </div>
</main>
