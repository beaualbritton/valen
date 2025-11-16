import type {PageServerLoad} from './$types'
import { fetchRepository } from '$lib/api/repository';

//'fetch' in params to invoke SvelteKit's special SSR fetch.
export const load : PageServerLoad = async ({ params, url, fetch}) => 
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

  return {
    username: user, 
    repoName: repository, 
    repoData: repoResponse,
    commits: commits,
    branches: branches,
    default: defaultBranch,
    currentOid: objectId
  }
}
