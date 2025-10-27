from pathlib import Path


GIT_ROOT = Path("/srv/git")

def create_user_dir(username: str) -> bool:
    parent_dir = Path(GIT_ROOT/username)
    if parent_dir.exists():
        return False
    else:
        parent_dir.mkdir(parents=True)
        return True


def get_user_dir(username: str) -> bool:
    user_dir = Path(GIT_ROOT/username)
    if user_dir.exists() and user_dir.is_dir():
        return True
    else:
        return False
