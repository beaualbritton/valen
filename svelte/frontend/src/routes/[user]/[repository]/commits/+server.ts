//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { fetchAllCommits } from '$lib/api/commits';

export const GET: RequestHandler = async ({ params, url }) => 
{
  //Destructuring username and repository from ../+page.svelte 
  const { user, repository } = params;

  //Important, calling on server
  const response = await fetchAllCommits(user, repository);

  return new Response(JSON.stringify(response), {headers: { 'Content-Type': 'application/json' }});
};
