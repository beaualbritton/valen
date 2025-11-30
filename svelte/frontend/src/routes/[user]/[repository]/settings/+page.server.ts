import type {PageServerLoad} from './$types'
import { getUser } from '$lib/api/login';
import { fetchRepoInfo } from '$lib/api/repository';

export const load : PageServerLoad = async ({cookies, params}) => 
{
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');

  const userResponse = await getUser({csrfToken, sessionId});
  let {currentUser} = userResponse;

  const {user, repository} = params;
  
  const infoResponse = await fetchRepoInfo(user, repository, {csrfToken, sessionId})
  let {response} = infoResponse;
  console.log(response)


  console.log('SERVER: csrfToken =', csrfToken);
  console.log('SERVER: sessionId =', sessionId);
  //TODO: Consider returning in a more elegant way
  return { response,user: currentUser};
}
