import { API_URL } from "$lib/config";

export async function addCollaborator(repository: string, collaborator: string, cookies: any)
{

  const { sessionId, csrfToken } = cookies;

  const apiResponse = await fetch(`${API_URL}/public/repo/collaborators/add/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
      credentials: "include", 
      body: JSON.stringify({repository, collaborator})
  });
  let collaboratorResponse= await apiResponse.json();
  console.log(collaboratorResponse)

  return {response: collaboratorResponse};
}

export async function removeCollaborator(repository: string, collaborator: string, cookies: any)
{

  const { sessionId, csrfToken } = cookies;

  const apiResponse = await fetch(`${API_URL}/public/repo/collaborators/remove/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken, 'Cookie': `sessionid=${sessionId}; csrftoken=${csrfToken}`},
      credentials: "include", 
      body: JSON.stringify({repository, collaborator})
  });
  let collaboratorResponse= await apiResponse.json();
  console.log(collaboratorResponse)

  return {response: collaboratorResponse};
}


export async function listCollaborator(repository: string)
{
  const apiResponse = await fetch(`${API_URL}/public/repo/collaborators/`, {
      method: "GET",
      headers: { "Content-Type": "application/json"},
      credentials: "include", 
      body: JSON.stringify({repository})
  });
  let collaboratorResponse= await apiResponse.json();
  console.log(collaboratorResponse)

  return {response: collaboratorResponse};
}
