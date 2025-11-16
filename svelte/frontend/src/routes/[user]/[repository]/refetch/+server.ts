//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { fetchRepository } from '$lib/api/repository';

export const GET: RequestHandler = async ({ params, url }) => 
{
  //Destructuring username and repository from ../+page.svelte 
  const { user, repository } = params;
  //If there is no oid then null, django handles null or no oid as 'HEAD' by default
  const objectId = url.searchParams.get('oid') || null;
  //Important, calling on server
  const response = await fetchRepository(user, repository, objectId);

  return new Response(JSON.stringify(response), {headers: { 'Content-Type': 'application/json' }});
};
