from pathlib import Path
GIT_ROOT = Path("/srv/git")


def create_user_dir(username: str) -> bool:
    try:
        parent_dir = Path(GIT_ROOT/username)
        if parent_dir.exists():
            return False
        else:
            parent_dir.mkdir(parents=True)
            return True
    except Exception:
        return False


def get_user_dir(username: str) -> bool:
    try:
        user_dir = Path(GIT_ROOT/username)
        if user_dir.exists() and user_dir.is_dir():
            return True
        else:
            return False
    except Exception:
        return False
