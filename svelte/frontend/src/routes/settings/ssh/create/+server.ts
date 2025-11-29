//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { addSSHKey } from '$lib/api/tokens';

export const POST: RequestHandler = async ({ cookies, request }) => 
{
  const { public_key } = await request.json();
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');
  console.log(public_key)
  const {response} = await addSSHKey(public_key, {csrfToken, sessionId});
  console.log(response)

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};

