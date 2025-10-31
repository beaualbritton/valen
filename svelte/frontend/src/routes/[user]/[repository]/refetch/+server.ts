//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from './$types';
import { fetchRepository } from '$lib/repository';

export const GET: RequestHandler = async ({ params, url }) => {
  const { user, repository } = params;
  const objectId = url.searchParams.get('oid') || null;

  const response = await fetchRepository(user, repository, objectId);

  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' }
  });
};
