<script lang="ts">
import AddCollaboratorForm from '$lib/components/dashboard/AddCollaboratorForm.svelte';
import CreateButton from '$lib/components/dashboard/CreateButton.svelte';
import { page } from '$app/state';

let { data } = $props<{ response: any; user: any}>();
console.log(data)

let collabData: any = $derived(data.response.data.collaborators)
let hasCollaborators: boolean = $derived(collabData.length > 0);
let isPublic = $state(data.response.data.public);

let privacySettings: boolean = $state(true);
let collaboratorSettings: boolean = $state(false);

const setPrivacySettings = (bool: boolean) => privacySettings = bool;
const setCollaboratorSettings = (bool: boolean) => collaboratorSettings = bool;

function handleSettingsToggle(setter: (b: boolean) => void)
{
  privacySettings = collaboratorSettings = false;
  setter(true)
}

let collaboratorFormToggle = $state(false);
let handleCollaboratorToggle = () => collaboratorFormToggle= !collaboratorFormToggle;
let path = (page.url.pathname).split("/");
let repository = path[2];
let owner = path[1];

async function handleCollaboratorDelete(collaborator: string)
{
  const creationResponse = await fetch(`/settings/repo/collaborators/remove`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ owner, repository, collaborator})
  });

  console.log(await creationResponse.json());
}

async function handlePrivacyToggle()
{
  const creationResponse = await fetch(`/settings/repo/privacy/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ owner, repository, isPublic})
  });

  console.log(await creationResponse.json());
}
</script>


<main class="bg-main flex flex-col justify-center items-center pt-16 overflow-x-hidden min-h-screen">
  <div class=" w-3/4 h-112 flex flex-row bg-elevated rounded-md border-2 border-main divide-x">
    <div class = "flex flex-col w-1/6 justify-center items-center gap-2">
      <button class = "hover:underline" onclick={() => handleSettingsToggle(setPrivacySettings)}>privacy</button>
      <button class = "hover:underline" onclick={() => handleSettingsToggle(setCollaboratorSettings)}>collaborators</button>
    </div>

    <div class = "h-auto flex flex-col justify-center items-center w-5/6 overflow-y-scroll">
      {@render settingsPanel()}
    </div>
  </div>
</main>

{#snippet settingsPanel()}
  {#if privacySettings}
    {@render privacyPanel()} 
  {:else if collaboratorSettings}
    {@render collaboratorPanel()} 
  {/if}
{/snippet}

{#snippet privacyPanel()}
<div class = "w-3/4">
  <div class="flex flex-row items-center justify-around">
    <div class = "w-2/3">
      <h2 class="pt-4 text-2xl font-bold text-green">Privacy</h2>
      <p class="text-muted text-sm">* change who sees your repo</p>
    </div>
    <div class="mt-6 w-1/3">
      <div class="flex items-center ">
        <!-- TODO: change repo visibility on change -->
        <select bind:value={isPublic} onchange={handlePrivacyToggle} class="flex-1 px-4 py-2 border-2 rounded bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm">
          <option value={true}>public</option>
          <option value={false} >private</option>
        </select>
      </div>
    </div>
  </div>
</div>
{/snippet}


{#snippet collaboratorPanel()}
<div class = "w-3/4">
  <div class="flex flex-row items-center justify-around">
    <div class = "w-2/3">
      <h2 class="pt-4 text-2xl font-bold text-green">Collaborators</h2>
      <p class="text-muted text-sm">* add or remove collaborators.</p>
    </div>
    <div class="mt-6 w-1/3">
      <CreateButton toggle={handleCollaboratorToggle} title="add collaborator"/>
    </div>
  </div>

  {#if collaboratorFormToggle}
    <AddCollaboratorForm toggle={collaboratorFormToggle} handleToggle={handleCollaboratorToggle} repository={repository} owner={owner}/>
  {/if}

  <div class="flex items-center justify-around mt-4">
  {#if hasCollaborators}
    <div class="flex-col items-center justify-center w-full">
      <div class="space-y-2 max-h-48 overflow-y-scroll">
        {#each collabData as collaborator}
          <div class="w-full p-3 rounded flex items-center justify-between bg-surface border border-main transition-all duration-150 hover:brightness-110 active:brightness-90 gap-2">
            <p class="text-main font-mono text-sm">{collaborator}</p>
            <button onclick={() => handleCollaboratorDelete(collaborator)} class="text-red text-sm">delete </button>
          </div>
        {/each}
      </div>
    </div>
  {:else}
  {/if}
  </div>

</div>
{/snippet}
