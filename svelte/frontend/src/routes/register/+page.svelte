<script lang="ts">
import LoginForm from "$lib/components/LoginForm.svelte";
import {register} from "$lib/api/login"
let status: any= $state();
let message: string = $state("")

// Binds to onSubmit in LoginForm.svelte. Binding functions allows for dynamic behavior.
async function registerSubmit(username: string, password: string, event: any)
{
  event.preventDefault();

  let registerResponse = await register(username, password);
  let response = registerResponse.response;

  status = response.status
  message = response.message
  console.log(response);

  return response 
}
</script>

<main class = "min-h-screen flex flex-row justify-center items-center  ">
  <div class = "flex flex-row justify-center items-center gap-1 text-shadow-md">

    <div class = "flex flex-col w-md">
      <h1 class="text-8xl text-nowrap">sign up.</h1>
      <h2 class = "text-lg italic p-2" 
          class:text-red-400={status==false} class:text-green-400={status==true} class:animate-pulse={status==false}> 
          {#if message} {message} 
          {:else} enter a username and password
          {/if}
      </h2>
    </div>

    <div class="flex flex-col items-center w-2xs ">
      <LoginForm onSubmit={registerSubmit}/>
    </div>

  </div>
</main>
