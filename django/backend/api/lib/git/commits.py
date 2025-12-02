from pygit2 import Repository, Commit, GIT_SORT_TIME, GIT_SORT_REVERSE
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
            if commit.id in visited_commits:
                continue
            visited_commits.add(commit.id)
            current_commit = commit.peel(Commit)
            commits.append({"oid": str(current_commit.id),"author": current_commit.author.name,"message": current_commit.message,"time": current_commit.commit_time})

    # was stuck on this one for a while, want to sort commits by commit_time, git_sort_time isn't doing this
    # see: https://stackoverflow.com/questions/72899/how-can-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary-in-python
    commits.sort(key=(lambda commit: commit["time"]), reverse=True)
    return Response({"status": True, "commits": commits})


# given an object id, walk the tree and find commits that contain object
def find_commit_refs(git_repo, git_object) -> Response:
    try:
        path = resolve_file_path(git_repo, git_object.id)

        if not path:
            return Response({"status": True, "commits": None})

        file_path, type_str = path
        is_tree = (type_str == "tree")
        prefix = f"{file_path}/" if is_tree and file_path else ""
        commits = []
        visited_commits = set()

        for branch in git_repo.branches.local:
            head = git_repo.branches[branch].target

            for commit in git_repo.walk(head, GIT_SORT_TIME):
                if commit.id in visited_commits:
                    continue
                visited_commits.add(commit.id)

                if not commit.parents:
                    if search_tree(git_repo, commit.tree, git_object.id):
                        commits.append({"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time})
                    continue

                parent = commit.parents[0]
                # pygit2 offers diff views for trees, see: https://www.pygit2.org/diff.html
                for patch in parent.tree.diff_to_tree(commit.tree):

                    new_path = patch.delta.new_file.path
                    old_path = patch.delta.old_file.path

                    # finding commits that modify or 'touch' a blob or tree
                    if not is_tree:
                        if new_path == file_path or old_path == file_path:
                            commits.append({"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time})
                            break
                    else:
                        if not file_path:
                            commits.append({"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time})
                            break
                        if (new_path.startswith(prefix) or old_path.startswith(prefix)):
                            commits.append({"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time})
                            break

        commits.sort(key=(lambda commit: commit["time"]), reverse=True)
        return Response({"status": True, "commits": commits})

    except Exception as e:
        return Response({"status": False, "commits": None, "message": f"error fetching {e}"})


# given an object id and a commit oid, find the latest commit that modified it relative to that commit
def find_latest_ref(git_repo, git_object, from_commit_oid) -> Response:
    try:
        latest_ref = None
        path = resolve_file_path(git_repo, git_object.id)
        if not path:
            return Response({"status": True, "commits": None}) 

        file_path, type_str = path
        is_tree = (type_str == "tree")
        prefix = f"{file_path}/" if is_tree and file_path else ""

        for commit in git_repo.walk(from_commit_oid, GIT_SORT_REVERSE):
            if not commit.parents:
                if search_tree(git_repo, commit.tree, git_object.id):
                    latest_ref = {"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time}
                continue

            parent = commit.parents[0]

            # pygit2 offers diff views for trees, see: https://www.pygit2.org/diff.html
            for patch in parent.tree.diff_to_tree(commit.tree):
                new_path = patch.delta.new_file.path
                old_path = patch.delta.old_file.path

                # finding commits that modify or 'touch' a blob or tree
                if not is_tree:
                    if new_path == file_path or old_path == file_path:
                        latest_ref = {"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time}
                else:
                    if not file_path:
                        latest_ref = {"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time}

                    if (new_path.startswith(prefix) or old_path.startswith(prefix)):
                        latest_ref = {"oid": str(commit.id), "author": commit.author.name, "message": commit.message, "time": commit.commit_time}

        return Response({"status": True, "commits": latest_ref})
    except Exception as e:
        return Response({"status": False, "error": str(e)})


# recursive tree search for latest refs
def search_tree(repo, tree, oid, path=""):
    if tree.id == oid:
        return (path or "", "tree")

    for entry in tree:
        entry_path = f"{path}/{entry.name}" if path else entry.name
        if entry.id == oid:
            return (entry_path, entry.type_str)
        elif entry.type_str == "tree":
            result = search_tree(repo, repo[entry.id], oid, entry_path)
            if result:
                return result
    return None


# finds the corresponding filepath for a git object
def resolve_file_path(repo, oid):
    for branch in repo.branches.local:
        branch_obj = repo.branches[branch]
        for commit in repo.walk(branch_obj.target, GIT_SORT_TIME):
            result = search_tree(repo, commit.tree, oid)
            if result:
                return result 
    return None
