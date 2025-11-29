//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { createToken } from '$lib/api/tokens';

export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { name, expirationDate } = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');
  const expiration = new Date(expirationDate);
  console.log(name)
  console.log(expirationDate)
  const {response} = await createToken(name, expiration, {csrfToken, sessionId});
  console.log(response)

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

