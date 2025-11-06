import { API_URL } from "$lib/config";

export async function fetchAllBranches(username: string, repository: string)
{
  let url = `${API_URL}/api/public/repo/branches/${username}/${repository}`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
  }); 

  let branchResponse = await apiResponse.json();

  return {response: branchResponse};
}

export async function fetchDefaultBranch(username: string, repository: string)
{
  let url = `${API_URL}/api/public/repo/branches/${username}/${repository}/default`

  const apiResponse = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json"},
  }); 

  let branchResponse = await apiResponse.json();

  return {response: branchResponse};

}
