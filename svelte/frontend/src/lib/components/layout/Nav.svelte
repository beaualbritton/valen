<script lang="ts">
import { logout } from "$lib/api/login";
import { goto } from "$app/navigation";
import { onMount } from "svelte";
import { page } from '$app/state';
let dropdownActive: boolean = $state(false);
let loggedIn: boolean = $state(false);
let loading: boolean = $state(true);
let user = $state("");
let path = $state("")

onMount(async () => { await checkAuthStatus(); });

$effect( () => { path = page.url.pathname; checkAuthStatus(); });

async function checkAuthStatus() 
{
  const response = await fetch('/server/fetch_user/');
  if (response.ok)
  {
    let userData = await response.json();

    console.log(userData);
    loggedIn= userData.status;

    if(loggedIn)
    {
      user = userData.user.username
    }

    loading = false
  }

  console.log(loggedIn)
  console.log(user)
}
const logoutAndRefresh = async() => {await logout(); location.reload();}
const handleDropdown = () => dropdownActive = !dropdownActive;
</script>

<nav class="flex flex-row justify-center items-center w-full h-12 bg-elevated shadow-xl border-b border-main fixed top-0 start-0 z-50">
  <div class="w-full px-8 flex flex-row justify-center items-center"> 
    <div class="flex flex-row w-1/2 justify-start items-center gap-2">
      <h1 class="text-2xl text-green font-bold"><a href="/">valen</a></h1>
      <span class = "text-lg text-yellow mt-0.5"> {#key path} {path} {/key}</span>
    </div>
    <div class="flex flex-row justify-end items-center w-3/4">
      {#if loading}
        <div class="text-main">Loading...</div>
      {:else if loggedIn}
        <div class="gap-4 flex flex-row items-center justify-baseline">
          <button class="bg-surface border border-main text-main h-9 rounded-md px-3 transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90" onclick={() => goto('/')}>dashboard</button>
          <button class="rounded-full border-2 border-main transition-all duration-150 hover:border-green focus:ring-2 focus:ring-green/50" onclick={handleDropdown} aria-label="User menu">
            <img src="https://braverplayers.org/wp-content/uploads/2022/09/blank-pfp.png" class="rounded-full w-9 h-9" alt="pfp">
          </button>
        </div>
        <div class="absolute mt-50 rounded-md h-36 flex flex-col shadow-lg items-center justify-start bg-surface border border-main divide-y w-32 py-2" style:visibility={dropdownActive ? 'visible' : 'hidden'}> 
          <div>
            <p class="p-0 mb-2 text-green">@{user}</p>
          </div>
          <div class = "flex flex-col items-center justify-center ">
            <a class="p-1 hover:underline" href="/{user}">profile</a>
            <a class="p-1 hover:underline" href="/settings">settings</a>
            <a class="p-1 hover:underline" href="/" onclick={async () => logoutAndRefresh()}>logout</a>
          </div>
        </div>
      {:else}
        <div class="gap-4 flex flex-row items-center">
          <button class="bg-surface border border-main text-green h-9 rounded-md px-3 transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90" onclick={() => goto('/login')}>sign in</button>
          <p>or</p>
          <button class="bg-surface border border-main text-yellow h-9 rounded-md px-3 transition-all duration-150 hover:brightness-110 active:scale-95 active:brightness-90" onclick={() => goto('/register')}>sign up</button>
        </div>
      {/if}
    </div>
  </div>
</nav>
