from pygit2 import Repository, Branch
from rest_framework.response import Response


# retrieves all branches for a repository
def get_branches(git_repo) -> Response:
    try:
        branch_list = []
        for branch_name in git_repo.branches:
            # something like list(repo.branches) returns STRS only, cant extract oid or any other metadata
            branch = git_repo.branches[branch_name]
            # pygit2 Branch class doesn't have id attribute. Just 'target'
            # https://www.pygit2.org/references.html#pygit2.Reference.target
            branch_list.append({"branch": branch_name,"oid": str(branch.target)})
        return Response({"status": True, "branches": branch_list})

    except Exception as e:
        return Response({"status": False, "branches": None, 
                         "message": f"error fetching branches: {e}"})


# get default branch from a repo: the branch that HEAD points to
def get_default_branch(git_repo: Repository) -> Response:
    try:
        head = git_repo.head.shorthand
        default_branch = git_repo.branches[head]
        default = {"branch": head, "oid": str(default_branch.target)}
        return Response({"status": True, "branches": default})

    except Exception as e:
        return Response({"status": False, "branches": None, 
                         "message": f"error fetching default branch: {e}"})
