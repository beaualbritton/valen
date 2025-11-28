<script lang="ts">
import RepoList from "$lib/components/repo_list/repo_list.svelte";
let { data } = $props<{ response: any; user: string }>();
let response = $state(data.response);
let user = $state(data.user)
console.log(user)
</script>

<!-- see: https://gitlab.uvm.edu/balbritt/cs399x-authenticate/-/blob/main/frontend/src/routes/profile/%5Buser%5D/+page.svelte?ref_type=heads -->
<main class="bg-main flex flex-col justify-center items-center pt-16 overflow-x-hidden min-h-screen" >
  <div class="w-3/4">
    <div class="w-full flex flex-row items-start justify-end gap-10 py-4">
      <div class="w-3/4 h-64 bg-elevated border border-main rounded-lg p-6">
        <h3 class="text-xl font-semibold text-green mb-3">About</h3>
      </div>
 
      <div class="flex w-1/4 flex-col items-center justify-start bg-elevated border border-main rounded-lg p-6">
        <img class="w-32 h-32 rounded-full border-2 border-main mb-4" alt="pfp" src="https://braverplayers.org/wp-content/uploads/2022/09/blank-pfp.png">
        <p class="text-xl font-bold text-main">{user}</p>
 
        <div class="flex flex-row gap-4 text-sm mb-4">
          <div class="text-center">
            <p class="text-main font-semibold">{response.repositories?.length} <span class="text-muted">repos</span></p>
          </div>
        </div>
      </div>
    </div>
 
    <div class="mt-6 w-full">
      <h3 class="text-xl font-semibold text-green mb-3">{user}'s repositories</h3>
      <RepoList repoList={response.repositories} user={user}/>
    </div>
  </div>
</main>
