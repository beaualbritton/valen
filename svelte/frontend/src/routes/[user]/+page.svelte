<script lang="ts">
import {createRepository} from "$lib/repository"

let repoToggle: boolean = $state(false);
let repoName : string = $state("");
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

<main class = "min-h-screen flex flex-row justify-center items-center text-shadow-md ">
  <div class = "flex flex-row justify-center items-center">
    <div class = "flex flex-col w-md">
      <h1 class="text-8xl text-nowrap"> hello, user</h1>
      
      <h2 class = "text-lg italic p-2 "> 
        create repository?
      </h2>
      <button onclick={toggle}>
        create
      </button>

      {#if repoToggle}
        <form onsubmit={submit}>
          <h1>repo name?</h1>
          <input bind:value={repoName}>
          <button type="submit">
            submit
          </button>
        </form>
      {/if}
    </div>

    <div class="flex flex-col items-center w-2xs">
    </div>
  </div>
</main>
