from pygit2 import Repository, Commit, GIT_SORT_TIME
from rest_framework.response import Response


# find all commits in a repo
def all_commits(git_repo) -> Response:
    commits = []
    for commit in git_repo.walk(git_repo.head.target, GIT_SORT_TIME):
        current_commit = commit.peel(Commit)
        commits.append({
            "oid": str(current_commit.id),
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
                    "oid": str(current_commit.id),
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
                    "oid": str(current_commit.id),
                    "author": current_commit.author.name,
                    "message": current_commit.message,
                    "time": current_commit.commit_time}
                break

    return Response({"status": True, "commits": latest_ref})
