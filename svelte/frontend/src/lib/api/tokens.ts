import { API_URL } from "$lib/config";
import { getCsrf } from "$lib/api/login";

export async function createToken(name: string, expiration: Date, cookies: any)
{

  const { sessionId, csrfToken } = cookies;

  const apiResponse = await fetch(`${API_URL}/public/token/create/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
      credentials: "include", 
      body: JSON.stringify({name, expiration: expiration.toISOString()})
  });
  let tokenResponse = await apiResponse.json();
  console.log(tokenResponse)

  return {response: tokenResponse};
}

export async function deleteToken(token: string, cookies: any)
{
  const { sessionId, csrfToken } = cookies;

  const apiResponse = await fetch(`${API_URL}/public/token/delete/`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
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

export async function addSSHKey(public_key: string, cookies: any)
{

  const { sessionId, csrfToken } = cookies;

  const apiResponse = await fetch(`${API_URL}/public/ssh/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
      credentials: "include", 
      body: JSON.stringify({public_key})
  });
  let keyResponse = await apiResponse.json();
  console.log(keyResponse)

  return {response: keyResponse};
}
