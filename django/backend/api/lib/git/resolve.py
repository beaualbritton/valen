# expects "git-*-pack ''/some/path/etc'"
def resolve_repo_path(command: str) -> str:
    command_args = command.split(" ",1)
    path = command_args[1].strip("'")
    path = path.split("/")
    return f"{path[-2]}/{path[-1]}"

