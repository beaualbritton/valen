[![Svelte](https://img.shields.io/badge/Svelte-%23f1413d.svg?logo=svelte&logoColor=white&style=for-the-badge)](#)
[![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white&style=for-the-badge)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)](#)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![SSH](https://img.shields.io/badge/SSH-yellow?logo=ssh&style=for-the-badge&logo=nginx&logoColor=white)
# `valen`
#### a distributed version control platform

<table >
  <tr><td><a href="#overview">Overview</a></td></tr>
  <tr><td><a href="#running locally">Local</a></td></tr>
  <tr><td><a href="#running on a server">Server</a></td></tr>
</table>

## Overview
Valen is a distributed version control platform I built over the span of a few months. It was my capstone project for a self-led independent study at my university.

#### Stack
* Django + DRF
* SvelteKit
* NGINX
* OpenSSH
* Docker

## Running Locally

Valen can be run locally with the provided `docker-compose.yml` file.

#### Prerequisites
* [Install Docker](docs.docker.com/engine/install/)
* [Django Key](https://www.educative.io/answers/how-to-generate-a-django-secretkey)
* [Configured Database](https://docs.djangoproject.com/en/6.0/ref/databases/)

#### Django
Docker handles dependencies when running with `docker-compose`, all that's necessary is to create an `.env` file in `./django/backend/`

```
#.env
secret_key=your-secret-key
database_url=postgresql://your-postgres-db/
```

#### Database
While developing this project, I used [supabase](https://supabase.com/) with an ipv4 pooler. They provide a [free tier](https://supabase.com/pricing) which should suffice for self-hosting. Otherwise, any other PostreSQL database will work fine.

## Running on a Server
See [prod/main](https://github.com/beaualbritton/valen/tree/prod/main?tab=readme-ov-file#running-on-a-server)

