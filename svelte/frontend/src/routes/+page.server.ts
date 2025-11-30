import type {PageServerLoad} from './$types'
import { getUser } from '$lib/api/login';

export const load : PageServerLoad = async ({cookies, fetch}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');


  const userResponse = await getUser({csrfToken, sessionId});
  let status: boolean = userResponse.currentUser.status
  let user = null;

  if(status)
  {
    user = userResponse.currentUser.user.username;
  }
  //TODO: Consider returning in a more elegant way
  return { user: user, status: status};
}
