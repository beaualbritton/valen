import type {PageServerLoad} from './$types'
import { fetchRepository } from '$lib/repository';

export const load : PageServerLoad = async ({ params, url }) => 
{
  const { user, repository } = params;

  const response = await fetchRepository(user, repository, null);
  return {username: user, repoName: repository, repoData: response}
}
