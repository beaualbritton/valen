import type { RequestHandler } from './$types';
import { getUser } from '$lib/api/login';


export const GET: RequestHandler = async ({ cookies}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');


  const userResponse = await getUser({csrfToken, sessionId});

  //TODO: Consider returning in a more elegant way
  return new Response(JSON.stringify(userResponse), {
    headers: { 'Content-Type': 'application/json' }
  });
};

