//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { deleteToken } from '$lib/api/tokens';

export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { token } = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');
  console.log(token);
  const {response} = await deleteToken(token, {csrfToken, sessionId});
  console.log(response)

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

