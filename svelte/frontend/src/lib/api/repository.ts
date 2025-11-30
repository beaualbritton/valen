import { API_URL } from "$lib/config";
import { getCsrf } from "$lib/api/login";

export async function createRepository(repository: string | null, description:string | null, visible: boolean | null, cookies: any)
{

  const { sessionId, csrfToken } = cookies;
  const apiResponse = await fetch(`${API_URL}/public/repo/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
    credentials: "include",
    body: JSON.stringify({ repository, description, visible})

  });

  let repositoryResponse = await apiResponse.json();
  return {response: repositoryResponse};

}

export async function fetchRepository(username:string, repository: string, objectId: string | null)
{
  let url = `${API_URL}/public/repo/by/${username}/${repository}`
  if (objectId !== null)
  {
    url = `${API_URL}/public/repo/by/${username}/${repository}/${objectId}`
  }
  
  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
    credentials: "include",
  }); 

  let repositoryResponse = await apiResponse.json();
  return {response: repositoryResponse};
}

export async function fetchAllRepositories(username: string, cookies: any)
{
  const { sessionId, csrfToken } = cookies;
  let url = `${API_URL}/public/repo/info/${username}`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
    credentials: "include",
  }); 

  let repositoryResponse = await apiResponse.json();
  return {response: repositoryResponse};
}

export async function fetchRepoInfo(username: string, repository: string, cookies: any)
{

  const { sessionId, csrfToken } = cookies;
  let url = `${API_URL}/public/repo/info/${username}/${repository}`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
    credentials: "include",
  }); 

  let repositoryResponse = await apiResponse.json();
  return {response: repositoryResponse};
}

export async function togglePrivacy(owner: string, repository: string, isPublic: boolean, cookies: any)
{

  const { sessionId, csrfToken } = cookies;
  let url = `${API_URL}/public/repo/privacy/`

  const apiResponse = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
    credentials: "include", 
    body: JSON.stringify({owner, repository, public: isPublic})
  }); 

  let privacyResponse = await apiResponse.json();
  return {response: privacyResponse};
}
