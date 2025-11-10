//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { fetchAllBranches} from '$lib/api/branches';

export const GET: RequestHandler = async ({ params, url }) => 
{
  //Destructuring username and repository from ../+page.svelte 
  const { user, repository } = params;

  //Important, calling on server
  const response = await fetchAllBranches(user, repository);

  return new Response(JSON.stringify(response), {headers: { 'Content-Type': 'application/json' }});
};
