<script lang="ts">
	import { page } from '$app/state';
</script>

<main class = "w-full min-h-screen flex flex-col items-center justify-center">
  <h1 class = "text-9xl font-semibold text-green">
    {page.status}<span class="ml-4 nf nf-dev-git text-s text-red"></span>
  </h1>

  <h2 class = "text-xl text-yellow mt-4">
    This route doesn't exist or is private. 
  </h2>
</main>


