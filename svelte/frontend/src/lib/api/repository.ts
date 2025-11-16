import { API_URL } from "$lib/config";
import { getCsrf } from "$lib/api/login";

export async function createRepository(repository: string)
{
  let csrfToken = await getCsrf();
  const apiResponse = await fetch(`${API_URL}/public/repo/create/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    credentials: "include",
    body: JSON.stringify({ repository })

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

export async function fetchAllRepositories(username: string)
{
  let url = `${API_URL}/public/repo/all/${username}/`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
    credentials: "include",
  }); 

  let repositoryResponse = await apiResponse.json();
  return {response: repositoryResponse};
}
