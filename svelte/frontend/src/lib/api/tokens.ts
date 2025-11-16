import { API_URL } from "$lib/config";
import { getCsrf } from "$lib/api/login";

export async function createToken(name: string, expiration: Date)
{

  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/public/token/create/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
      credentials: "include", 
      body: JSON.stringify({name, expiration: expiration.toISOString()})
  });
  let tokenResponse = await apiResponse.json();

  return {response: tokenResponse};
}

export async function deleteToken(token: string)
{
  let csrfToken = await getCsrf()
  const apiResponse = await fetch(`${API_URL}/public/token/create/`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
      credentials: "include",
      body: JSON.stringify({ token })
  });

  let tokenResponse = await apiResponse.json();

  return {response: tokenResponse};
}

export async function listTokens(cookies: any)
{
  const { sessionId, csrfToken } = cookies;
  const apiResponse = await fetch(`${API_URL}/public/token/list/`, {
      method: "GET",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
  });
  let tokenResponse = await apiResponse.json();

  return {response: tokenResponse};
}
