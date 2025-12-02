import { API_URL } from "$lib/config";

export async function fetchAllCommits(username: string, repository: string)
{
  let url = `${API_URL}/public/repo/commits/${username}/${repository}`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
  }); 

  let commitResponse = await apiResponse.json();

  return {response: commitResponse};
}

export async function fetchLatestCommitForObject(username: string, repository: string, oid: string | null, fromCommitOID: string | null)
{
  let url = `${API_URL}/public/repo/commits/${username}/${repository}/${oid}/${fromCommitOID}/`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
  }); 

  let commitResponse = await apiResponse.json();

  console.log(commitResponse);
  return {response: commitResponse};
}


