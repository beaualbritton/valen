<script lang="ts">
let {toggle, title= $bindable()} : {toggle(): void, title: string} = $props()

</script>

<button onclick={toggle} class="bg-surface border border-main text-main px-4 py-2 rounded font-medium transition-all duration-150 active:scale-95 active:brightness-90 hover:brightness-110">
  {title}
</button>
