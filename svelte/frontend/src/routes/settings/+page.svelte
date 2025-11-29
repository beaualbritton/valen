<script lang="ts">
import CreateTokenForm from '$lib/components/dashboard/CreateTokenForm.svelte';
import CreateSSHForm from '$lib/components/dashboard/CreateSSHForm.svelte';
import CreateButton from '$lib/components/dashboard/CreateButton.svelte';
let { data } = $props<{ response: any; user: any}>();
console.log(data)

let hasTokens = $derived(data.response.status);

let tokenResponse: any = $state(null);
let setToken = (token: string) => tokenResponse = token;
let tokenData: any = $derived(data.response.tokens)

let profileSettings: boolean = $state(false);
let tokenSettings: boolean = $state(true);
let sshSettings: boolean = $state(false);

const setProfileSettings = (bool: boolean) => profileSettings = bool;
const setTokenSettings = (bool: boolean) => tokenSettings = bool;
const setSSHSettings = (bool: boolean) => sshSettings = bool;

function handleSettingsToggle(setter: (b: boolean) => void)
{
  profileSettings = tokenSettings = sshSettings = false;
  setter(true)
}

let tokenFormToggle = $state(false);
let handleTokenToggle = () => tokenFormToggle = !tokenFormToggle;

let sshFormToggle = $state(false);

let handleSSHToggle = () => sshFormToggle = !sshFormToggle;

async function handleTokenDelete(token: string)
{
  const creationResponse = await fetch(`/settings/token/delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token })
  });

  console.log(await creationResponse.json());
}

</script>


<main class="bg-main flex flex-col justify-center items-center pt-16 overflow-x-hidden min-h-screen">
  <div class=" w-3/4 h-112 flex flex-row bg-elevated rounded-md border-2 border-main divide-x">
    <div class = "flex flex-col w-1/6 justify-center items-center gap-2">
      <button class = "hover:underline" onclick={() => handleSettingsToggle(setTokenSettings)}>tokens</button>
      <button class = "hover:underline" onclick={() => handleSettingsToggle(setSSHSettings)}>ssh keys</button>
    </div>

    <div class = "h-auto flex flex-col justify-center items-center w-5/6 overflow-y-scroll">
      {@render settingsPanel()}
    </div>
  </div>
</main>

{#snippet settingsPanel()}
  {#if tokenSettings}
    {@render tokenPanel()} 
  {:else if sshSettings}
    {@render sshPanel()} 
  {/if}
{/snippet}


{#snippet profilePanel()}
  <!--TODO: implement-->
  * coming soon
{/snippet}

{#snippet tokenPanel()}
<div class = "w-full">
  <div class="flex flex-row items-center justify-around">
    <div>
      <h2 class="pt-4 text-2xl font-bold text-green">Access Tokens</h2>
      <p class="text-muted text-sm">* personal access tokens are used for https operations</p>
    </div>
    <div class="mt-8">
      <CreateButton toggle={handleTokenToggle} title="create token"/>
    </div>
  </div>

  {#if tokenFormToggle}
    <CreateTokenForm toggle={tokenFormToggle} handleToggle={handleTokenToggle} setToken={setToken}/>
  {/if}

  {#if tokenResponse}
    <div class="flex flex-row justify-around items-center gap-3 mt-4">
      <div class="flex-col w-7/8">
        <p class="text-yellow font-semibold mb-1">Copy this token!</p>
        <p class="text-muted text-sm">You won't be able to see it again.</p>
        <div class="bg-main border border-main rounded px-3 py-2 font-mono text-sm">{tokenResponse}</div>
      </div>
    </div>
  {/if}
  
  <div class="flex items-center justify-around mt-4">
  {#if hasTokens}
    <div class="flex-col items-center justify-center w-7/8">
      <h3 class="text-lg font-semibold text-green italic mb-3">Your Tokens</h3>
      <div class="space-y-2 max-h-48 overflow-y-scroll">
        {#each tokenData as token}
          <div class="w-full p-3 rounded flex items-center justify-between bg-surface border border-main transition-all duration-150 hover:brightness-110 active:brightness-90 gap-2">
            <p class="text-main font-mono text-sm">{token}</p>
            <button onclick={() => handleTokenDelete(token)} class="text-red text-sm">delete </button>
          </div>
        {/each}
      </div>
    </div>
  {:else}
  {/if}
  </div>
</div>
{/snippet}


{#snippet sshPanel()}
<div class = "w-full">
  <div class="flex flex-row items-center justify-around">
    <div>
      <h2 class="pt-4 text-2xl font-bold text-green">SSH Keys</h2>
      <p class="text-muted text-sm">* ssh keys are used for git ssh operations.</p>
    </div>
    <div class="mt-8">
      <CreateButton toggle={handleSSHToggle} title="add ssh key"/>
    </div>
  </div>

  {#if sshFormToggle}
    <CreateSSHForm toggle={sshFormToggle} handleToggle={handleSSHToggle}/>
  {/if}
</div>
{/snippet}
