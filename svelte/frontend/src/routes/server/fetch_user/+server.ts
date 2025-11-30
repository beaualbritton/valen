import type { RequestHandler } from './$types';
import { getUser } from '$lib/api/login';


export const GET: RequestHandler = async ({ cookies}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');


  const userResponse = await getUser({csrfToken, sessionId});
  let {currentUser} = userResponse;

  //TODO: Consider returning in a more elegant way
  return new Response(JSON.stringify(currentUser), {
    headers: { 'Content-Type': 'application/json' }
  });
};

