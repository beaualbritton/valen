//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { togglePrivacy } from '$lib/api/repository';
export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { owner, repository, isPublic} = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');

  const {response} = await togglePrivacy(owner, repository, isPublic, {csrfToken, sessionId});
  console.log(response)

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

