<script lang="ts">
let {toggle, handleToggle, user= $bindable()} : {toggle:boolean, handleToggle(): void, user:string}= $props()
let repository = $state("");
let description = $state("");
let visible = $state(true);

async function submit(e: Event)
{
  e.preventDefault();
  const refetchResponse = await fetch(`/${user}/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repository, description, visible })
  });

  console.log(await refetchResponse.json());

  handleToggle()
}
</script>

{#if toggle}
  <div class="fixed inset-0 flex items-center justify-center bg-main/50 z-50 animate-fade-in p-4">
    <div class="bg-surface rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
      <form method="post" onsubmit={submit} class="p-6 md:p-8">
        <div class="flex items-center justify-between mb-8">
          <h2 class = "text-3xl font-bold px-5">new repository</h2>
          <button onclick={handleToggle} class ="text-red hover:brightness-110 focus:brightness-90 transition-colors"aria-label="Close">
            <span class = "nf nf-fa-close text-xl"></span>
          </button>
        </div>
        <div class="w-full flex justify-center">
          <div class="w-xl space-y-4">
            <div class="flex items-center gap-4">
              <p class="text-xl whitespace-nowrap px-1">{user} /</p>
              <input bind:value={repository} type="text" placeholder="name your repository" required class="flex-1 px-4 py-3 border-2 rounded-xl bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm resize-none" />
            </div>

            <div>
              <textarea bind:value={description} rows={3} placeholder="description" required class="w-full px-4 py-3 border-2 rounded-xl bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm resize-none"></textarea>
            </div>

            <div class="flex items-center gap-4">
              <select bind:value={visible} class="flex-1 px-4 py-3 border-2 rounded-xl bg-surface brightness-95 text-main focus:outline-none active:outline-none focus:ring-2 focus:ring-[#a7c080] shadow-sm">
                <option value={true}>public (default)</option>
                <option value={false} >private</option>
              </select>
            </div>
            <p class = "text-sm px-2 italic text-muted">* this can be changed later</p>
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
