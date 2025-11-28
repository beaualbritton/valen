//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { createRepository } from '$lib/api/repository';

export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { repository, description, visible } = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');


  const response = await createRepository(repository, description, visible, {csrfToken, sessionId});

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

