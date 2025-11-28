<script lang="ts">
import { HighlightAuto } from "svelte-highlight";
import gruvboxDarkHard from "svelte-highlight/styles/gruvbox-dark-hard";
let { blob = $bindable()} : {blob: any } = $props()
let code = blob.entries.split("\n").join("\n");
</script>

<svelte:head>
  {@html gruvboxDarkHard}
</svelte:head>

<section class="w-xl bg-elevated border border-main rounded-lg overflow-hidden">
  <div class="h-96 overflow-auto">
    <HighlightAuto {code} />
  </div>
</section>
