//See: https://svelte.dev/docs/kit/routing
import type { RequestHandler } from "@sveltejs/kit";

export const GET: RequestHandler = () => 
{
    return new Response('OK', { status: 200 });
};
