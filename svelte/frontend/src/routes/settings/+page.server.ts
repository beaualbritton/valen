import type {PageServerLoad} from './$types'
import { listTokens } from '$lib/api/tokens'
import { getUser } from '$lib/api/login';
export const load : PageServerLoad = async ({cookies}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');

  const tokens = await listTokens({csrfToken, sessionId}); 
  let {response} = tokens;

  const userResponse = await getUser({csrfToken, sessionId});
  let {user} = userResponse;

  //TODO: Consider returning in a more elegant way
  return { response: response, user: user};
}
