<script lang="ts">
import FileTree from "$lib/components/file_tree/file_tree.svelte";
let {data} = $props()
let repository = $state(data.repoData)
let user = $state(data.username)
let repoName = $state(data.repoName)
let root = $derived(repository.response.object)
let commits = $state(data.commits.response.commits)
let branches = $state(data.branches.response.branches)
let defaultBranch = $state(data.default.response.branches)
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
  <div class = "min-h-screen flex flex-col items-center justify-center">
    <div>
      <table>
        <thead>
          <tr><th>commits</th></tr>
        </thead>
        <tbody>

          <!--TODO: make this a component-->
            {#each commits as commit}
              <tr>
                <td><a onclick={() => refetch(commit.oid)} class="hover:underline">{commit?.author}: {commit?.message} @ {new Date(commit?.time * 1000).toLocaleDateString()}</a></td>
              </tr>
            {/each}
        </tbody>
      </table>
      <table>
        <thead>
          <tr><th>branches</th></tr>
        </thead>
        <tbody>
            <tr>
              <td><a onclick={() => refetch(defaultBranch.oid)} class="hover:underline">default:{defaultBranch.branch}</a></td>
            </tr>
          <!--TODO: make this a component-->
            {#each branches as branch}
              <tr>
                <td><a onclick={() => refetch(branch.oid)} class="hover:underline">{branch.branch}</a></td>
              </tr>
            {/each}
        </tbody>
      </table>
    </div>
    <FileTree root={root} handleRefetch={refetch} getLatest={getLatestFromObject}/>
  </div>
 </main>
