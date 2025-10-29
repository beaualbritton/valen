from pygit2 import Repository, Commit, Tree
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
