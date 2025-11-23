# expects "git-*-pack ''/some/path/etc'"
def resolve_repo_ssh(command: str) -> str:
    command_args = command.split(" ",1)
    path = command_args[1].strip("'")
    path = path.split("/")
    return f"{path[-2]}/{path[-1]}"


# expects /git/doodle/test7/git-upload-pack
def resolve_repo_http(command: str) -> str:
    command_args = command.split("/")
    command_args.remove('')
    user = command_args[1]
    repo = command_args[2]

    return f"{user}/{repo}"
