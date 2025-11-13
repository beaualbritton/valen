<script lang="ts">
import LoginForm from "$lib/login/LoginForm.svelte";
import { goto } from "$app/navigation";
import {login} from "$lib/api/login";

let status: any = $state();
// Binds to onSubmit in LoginForm.svelte. Binding functions allows for dynamic behavior.
async function loginSubmit(username: string, password: string, event: any)
{
  event.preventDefault();
  //Calling login functions from frontend/lib/login
  let loginResponse = await login(username, password);
  let response = loginResponse.response;
  status = response.status;
  console.log(response)
  if(response.status == true)
  {
    setTimeout(()=> goto(`/${username}/`), 1000);
  }
  return response;
}
</script>

<main class = "min-h-screen flex flex-row justify-center items-center text-shadow-md ">
  <div class = "flex flex-row justify-center items-center">
    <div class = "flex flex-col w-md">
      <h1 class="text-8xl text-nowrap"> {#if status}signed in! {:else }sign in.{/if}</h1>
      
      <h2 class = "text-lg italic p-2 "
          class:text-red-400={status==false} class:text-green-400={status==true} class:animate-pulse={status==false}> 
          {#if status == false} invalid login.
          {:else if status ==true} you may enter.
          {:else} what's the password?
          {/if}
      </h2>
    </div>

    <div class="flex flex-col items-center w-2xs">
    <LoginForm bind:onSubmit={loginSubmit}/>
    </div>
  </div>
</main>
