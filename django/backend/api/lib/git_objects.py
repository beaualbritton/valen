from pygit2 import Repository, Commit, Tree, GIT_SORT_TIME
from rest_framework.response import Response


def peel_commit(git_object) -> Response:
    try: 
        current_object = git_object.peel(Commit)
        entry_list = []

        for entry in current_object.tree:
            entry_list.append({
                "name": entry.name,
                "type": entry.type_str,
                "oid": str(entry.id),
            })

        return Response({
            "status": True,
            "object":
            {
                "type": current_object.type_str,
                "oid": str(current_object.id),
                "name": current_object.name,
                "message": current_object.message,
                "author": current_object.author.name,
                "time":  str(current_object.commit_time),
                "entries": entry_list,
            }
        })
    except Exception as error:
        return Response({"status": False, "message": f"error: {error}"})


def peel_tree(git_object) -> Response:
    try:
        current_object = git_object.peel(Tree)
        entry_list = []

        for entry in current_object:
            entry_list.append({
                "name": entry.name,
                "type": entry.type_str,
                "oid": str(entry.id),
            })

        return Response({
            "status": True,
            "object":
            {
                "type": current_object.type_str,
                "oid": str(current_object.id),
                "name": current_object.name,
                "entries": entry_list,
            }
        })
    except Exception as error:
        return Response({"status": False, "message": f"error: {error}"})


def peel_blob(git_object) -> Response:
    current_object = git_object
    try:
        return Response({
            "status": True,
            "object":
            {
                "type": current_object.type_str,
                "oid": str(current_object.id),
                "name": current_object.name,
                "entries": current_object.data.decode('utf-8')
            }
        })
    except Exception as error:
        return Response({"status": False, "message": f"error: {error}"})


# find all commits in a repo
def all_commits(git_repo) -> Response:
    commits = []
    for commit in git_repo.walk(git_repo.head.target, GIT_SORT_TIME):
        current_commit = commit.peel(Commit)
        commits.append({
            "oid": current_commit.id,
            "author": current_commit.author.name,
            "message": current_commit.message,
            "time": current_commit.commit_time})

    return Response({"status": True, "commits": commits})


# given an object id, walk the tree and find commits that contain object
def find_commit_refs(git_repo, git_object):
    commit_refs = []
    for commit in git_repo.walk(git_repo.head.target, GIT_SORT_TIME):
        current_commit = commit.peel(Commit)
        for entry in commit.tree:
            if entry.id == git_object.id:
                commit_refs.append({
                    "oid": current_commit.id,
                    "author": current_commit.author.name,
                    "message": current_commit.message,
                    "time": current_commit.commit_time})

    return Response({"status": True, "commits": commit_refs})


# given an object id, find the first commit that contains object
def find_latest_ref(git_repo, git_object) -> Response:
    latest_ref = None
    for commit in git_repo.walk(git_repo.head.target, GIT_SORT_TIME):
        current_commit = commit.peel(Commit)
        for entry in commit.tree:
            if entry.id == git_object.id:
                latest_ref = {
                    "oid": current_commit.id,
                    "author": current_commit.author.name,
                    "message": current_commit.message,
                    "time": current_commit.commit_time}
                break

    return Response({"status": True, "commits": latest_ref})
