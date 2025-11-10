<script lang="ts">
import { HighlightAuto } from "svelte-highlight";
import gruvboxLightHard from "svelte-highlight/styles/gruvbox-light-hard";
let { blob = $bindable()} : {blob: any } = $props()

let code = blob.entries.split("\n").join("\n");
</script>

<svelte:head>
  {@html gruvboxLightHard}
</svelte:head>

<section class = "h-64 overflow-scroll rounded-lg">
  <HighlightAuto {code} />
</section>
