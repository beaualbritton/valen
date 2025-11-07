<script lang="ts">
let { blob = $bindable()} : {blob: any } = $props()

let markdown = $derived(blob.entries.split("\n") || ' ');
</script>

<section class = "h-64 overflow-scroll">
  {@html markdown}
</section>
