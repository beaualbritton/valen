from pygit2 import Repository, Commit, GIT_SORT_TIME
from rest_framework.response import Response


# find all commits in a repo
def all_commits(git_repo) -> Response:
    commits = []
    visited_commits = set()

    for branches in git_repo.branches.local:
        branch = git_repo.branches[branches]
        branch_oid = branch.target

        for commit in git_repo.walk(branch_oid, GIT_SORT_TIME):
            # if commit has already been visited -- skip
            if commit in visited_commits:
                continue
            visited_commits.add(commit.id)
            current_commit = commit.peel(Commit)
            commits.append({
                "oid": str(current_commit.id),
                "author": current_commit.author.name,
                "message": current_commit.message,
                "time": current_commit.commit_time})

    # was stuck on this one for a while, want to sort commits by commit_time, git_sort_time isn't doing this
    # see: https://stackoverflow.com/questions/72899/how-can-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
    commits.sort(key=(lambda commit: commit["time"]), reverse=True)
    return Response({"status": True, "commits": commits})


# given an object id, walk the tree and find commits that contain object
def find_commit_refs(git_repo, git_object):
    commit_refs = []
    visited_commits = set()

    for branches in git_repo.branches.local:
        branch = git_repo.branches[branches]
        branch_oid = branch.target

        for commit in git_repo.walk(branch_oid, GIT_SORT_TIME):
            # if commit has already been visited -- skip, some commits are shared
            if commit in visited_commits:
                continue
            visited_commits.add(commit.id)
            current_commit = commit.peel(Commit)

            if contains_object(git_repo, current_commit.tree, git_object.id):
                commit_refs.append({
                    "oid": str(current_commit.id),
                    "author": current_commit.author.name,
                    "message": current_commit.message,
                    "time": current_commit.commit_time
                })
    return Response({"status": True, "commits": commit_refs})


# given an object id, find the first commit that contains object
def find_latest_ref(git_repo, git_object) -> Response:
    latest_ref = None
    visited_commits = set()

    for branches in git_repo.branches.local:
        branch = git_repo.branches[branches]
        branch_oid = branch.target

        for commit in git_repo.walk(branch_oid, GIT_SORT_TIME):
            # if commit has already been visited -- skip, some commits are shared
            if commit in visited_commits:
                continue
            visited_commits.add(commit.id)
            current_commit = commit.peel(Commit)

            if contains_object(git_repo, current_commit.tree, git_object.id):
                latest_ref = {
                    "oid": str(current_commit.id),
                    "author": current_commit.author.name,
                    "message": current_commit.message,
                    "time": current_commit.commit_time}
                break
    return Response({"status": True, "commits": latest_ref})


# recursive tree search for latest refs
def contains_object(repo, tree, oid):
    for entry in tree:
        if entry.id == oid:
            return True
        elif entry.type_str == "tree":
            subtree = repo[entry.id]
            if contains_object(repo, subtree, oid):
                return True
    return False
