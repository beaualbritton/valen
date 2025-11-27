<script lang="ts">
let username: string = $state("");
let password: string = $state("");
let response: any = $state();

let {onSubmit = $bindable()} : {onSubmit: (username: string, password: string, event: any) => void; } = $props()
async function handleSubmit(event: any)
{
  event.preventDefault();

  response = await onSubmit(username,password,event);
}


</script>
<form onsubmit={handleSubmit} class=" p-6 bg-black/20 rounded-md flex flex-col items-center lg drop-shadow-2xl">
    <div class = "justify-center items-center flex flex-col text-xl">
      <label class = "">
        <input class="bg-black/10 rounded-sm p-2 m-2" placeholder="username" bind:value={username}/>
      </label>

      <div class = "bg-stone-500/90 w-48 rounded-lg m-2 h-0.25"></div>

      <label class = "">
        <input type="password" class="bg-black/10 rounded-sm p-2 m-2" placeholder="password" bind:value={password} />
      </label>
      <button class="btn mt-4" type="submit" onsubmit={handleSubmit}>
        submit
      </button>
    </div>
</form>
