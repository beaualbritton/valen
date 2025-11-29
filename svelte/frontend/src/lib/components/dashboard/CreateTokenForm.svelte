<script lang="ts">
let {toggle, handleToggle, setToken= $bindable()} : {toggle:boolean, handleToggle(): void, setToken: any}= $props()
let name = $state("");
let expirationDays: any = $state();

async function submit(e: Event)
{
  e.preventDefault();


  const expirationDate: Date = new Date(Date.now() + (expirationDays * 24 * 60 * 60 * 1000));

  const creationResponse = await fetch(`/settings/token/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, expirationDate})
  });

  const tokenData = await creationResponse.json();
  setToken(tokenData.token);

  handleToggle()
}
</script>

{#if toggle}
  <div class="fixed inset-0 flex items-center justify-center bg-main/50 z-50 animate-fade-in p-4 pt-16">
    <div class="bg-surface rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <form method="post" onsubmit={submit} class="p-6 md:p-8">
        <div class="flex items-center justify-between mb-8">
          <h2 class = "text-3xl font-bold px-5">new token</h2>
          <button onclick={handleToggle} class ="text-red hover:brightness-110 focus:brightness-90 transition-colors"aria-label="Close">
          </button>
        </div>
        
        
        <div class="w-full flex justify-center">
          <div class="w-xl space-y-4">
            <div class="flex items-center gap-4">
              <input bind:value={name} type="text" placeholder="name your token" required class="flex-1 px-4 py-3 border-2 rounded-xl bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm resize-none" />
            </div>

            <p class = "text-md px-2 italic text-muted">Expiration</p>
            <div class="flex items-center gap-4">
              <select bind:value={expirationDays} class="flex-1 px-4 py-3 border-2 rounded-xl bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm">
                <option value={7}>7 days</option>
                <option value={30}>30 days </option>
                <option value={60}>60 days </option>
                <option value={90}>90 days </option>
                <option value={99999}>No expiration (insecure)</option>
              </select>
            </div>
          </div>
        </div>

        <div class ="flex justify-end gap-3 mt-8 pt-6 border-t">
          <button onclick={handleToggle} class="bg-surface border border-main text-red px-4 py-2 rounded font-medium transition-all duration-150 active:scale-95 active:brightness-90 hover:brightness-110">
            Cancel
          </button>
          <button type="submit" class="bg-surface border border-main text-green px-4 py-2 rounded font-medium transition-all duration-150 active:scale-95 active:brightness-90 hover:brightness-110">
            Create
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
<!-- TODO: banner for success/fail-->
