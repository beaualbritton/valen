<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
  import Navbar from '$lib/components/layout/Nav.svelte';
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
  <link rel="stylesheet" href="https://www.nerdfonts.com/assets/css/webfont.css">
</svelte:head>

<Navbar/>
{@render children()}
