//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { listCollaborator} from '$lib/api/collaborators';

export const POST: RequestHandler = async ({ request }) => 
{
  const { owner, repository } = await request.json();

  const {response} = await listCollaborator(owner, repository);

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

