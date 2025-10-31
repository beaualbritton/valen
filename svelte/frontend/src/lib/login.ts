import { API_URL } from "./config";
let csrf : string;
export async function getCsrf()
{
  const csrfResponse= await fetch(`${API_URL}/api/csrf/`
, {
    credentials: "include"
  });

  let data = await csrfResponse.json();
  csrf = data.csrfToken;

  return csrf; 
}

export async function login(username : string, password: string)
{
  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/api/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    //cookies for session 
    credentials: "include",
    body: JSON.stringify({ username,password }),
  });
  let loginResponse = await apiResponse.json();
  
  return {response: loginResponse};
}
export async function logout()
{
  let csrfToken = await getCsrf();

  const apiResponse = await fetch(`${API_URL}/api/logout/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken},
    //cookies for session 
    credentials: "include",
  });
  let logoutResponse = await apiResponse.json();

  return {response: logoutResponse};
}
export async function register(username:string, password: string)
{
  const apiResponse = await fetch(`${API_URL}/api/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username,password }),
  });
  let registerResponse = await apiResponse.json();
  console.log(registerResponse)

  return {response: registerResponse};
}
