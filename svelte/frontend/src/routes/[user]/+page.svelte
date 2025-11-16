<script lang="ts">
import {createRepository} from "$lib/api/repository"
import RepoList from "$lib/components/repo_list/repo_list.svelte";
let { data } = $props<{ response: any; user: string }>();
let response = $state(data.response);
let user = $state(data.user)
console.log(user)
let repoToggle: boolean = $state(false);
let repoName : string = $state("test");

function toggle() : void
{
  repoToggle = !repoToggle;
}

async function submit(e: any)
{
  e.preventDefault();
  let response = await createRepository(repoName);
  console.log(response);

}
</script>

<main >
  <div class = "min-h-screen flex justify-start items-center text-shadow-md ">
    <div class = "min-h-screen flex flex-col w-1/2">
      <h2 class = "text-2xl">{user}'s repositories</h2>
      <RepoList repoList={response.repositories} user={user}/>
      <button onclick={submit}>
        new repo?
      </button>
    </div>
  </div>
</main>
