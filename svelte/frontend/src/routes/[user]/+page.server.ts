import type {PageServerLoad} from './$types'
import { fetchAllRepositories } from '$lib/api/repository';
import { redirect } from '@sveltejs/kit'
/*
 * See: https://svelte.dev/docs/kit/load
 *
 * Loading data on the server-side to save the client some work (when javascript gets dense). This is a proactive approach,
 * as I found that the smallest features required a decent bit of javascript (typescript, in this case) to interact with Django.
*/
export const load : PageServerLoad = async ({params,cookies}) => 
{
  const username = params.user;
  
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');


  const repoResponse = await fetchAllRepositories(username, {csrfToken, sessionId}); 
  let {response} = repoResponse;

  console.log(response)
  //TODO: Consider returning in a more elegant way
  return { response, user: username};
}
