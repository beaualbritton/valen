import type {PageServerLoad} from './$types'
import { fetchRepository } from '$lib/repository';

export const load : PageServerLoad = async ({ params, url }) => 
{
  const { user, repository } = params;
  let objectId = url.searchParams.get('oid') || null;
  
  const response = await fetchRepository(user, repository, objectId);
  return {
    username: user, 
    repoName: repository, 
    repoData: response,
    currentOid: objectId
  }
}
