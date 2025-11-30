//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { removeCollaborator } from '$lib/api/collaborators';

export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { owner, repository, collaborator } = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');
  console.log(repository)

  const {response} = await removeCollaborator(owner, repository, collaborator, {csrfToken, sessionId});
  console.log(response)

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

