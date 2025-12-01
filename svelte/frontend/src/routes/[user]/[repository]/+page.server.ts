import type {PageServerLoad} from './$types'
import { fetchRepository } from '$lib/api/repository';
import { getUser } from '$lib/api/login';
import { fetchRepoInfo } from '$lib/api/repository';
import { error } from '@sveltejs/kit';
//'fetch' in params to invoke SvelteKit's special SSR fetch.
export const load : PageServerLoad = async ({ params, url, fetch, cookies}) => 
{
  const { user, repository } = params;
  let objectId = url.searchParams.get('oid') || null;
  
  const repoResponse = await fetchRepository(user, repository, objectId);
  
  const commitResponse = await fetch(`/${user}/${repository}/commits`);
  const commits = await commitResponse.json();

  const allBranchResponse = await fetch(`/${user}/${repository}/branches`);
  const branches = await allBranchResponse.json();

  const defaultBranchResponse= await fetch(`/${user}/${repository}/branches/default`);
  const defaultBranch = await defaultBranchResponse.json();
  
  const csrfToken = cookies.get('csrftoken');
  const sessionId = cookies.get('sessionid');

  const userResponse = await getUser({csrfToken, sessionId});
  let {currentUser} = userResponse;

  const infoResponse = await fetchRepoInfo(user, repository, {csrfToken, sessionId})
  let {response} = infoResponse;
  console.log(response)
  
  const isPublic = response.data.public;
  const owner = response.data.owner;
  const current = currentUser.user.username;
  const collaborators = response.data.collaborators;
  if(isPublic)
  {
    if(!((current === owner) || (collaborators.includes(current))))
    {
      throw error(404, 'Not Found');
    }
  }

  return {
    username: user, 
    repoName: repository, 
    repoData: repoResponse,
    commits: commits,
    branches: branches,
    default: defaultBranch,
    currentOid: objectId,
    currentUser
  }
}
