import type {PageServerLoad} from './$types'
import { listTokens } from '$lib/api/tokens'
import { getUser } from '$lib/api/login';
export const load : PageServerLoad = async ({cookies, fetch}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');

  const tokens = await listTokens({csrfToken, sessionId}); 
  let {response} = tokens;

  const userResponse = await getUser({csrfToken, sessionId});
  let {user} = userResponse;

  console.log('SERVER: csrfToken =', csrfToken);
  console.log('SERVER: sessionId =', sessionId);
  //TODO: Consider returning in a more elegant way
  return { response: response, user: user};
}
