#!/usr/bin/env python3
import os, sys, json
from urllib.request import Request, urlopen

# set user and cmd from system environment 
user = os.getenv("SSH_USER")
cmd = os.getenv("SSH_ORIGINAL_COMMAND")

if not user or not cmd:
    sys.exit(1)

header = {"Content-Type": "application/json"}
body = json.dumps({"username": user, "command": cmd}).encode()
request = Request("http://backend:8000/api/auth/ssh/", data=body, headers=header, )

try:
    response = urlopen(request, timeout=10)
    allowed = json.loads(response.read()).get("allowed", False)
except Exception:
    sys.exit(1)

if allowed:
    os.execvp("git-shell", ["git-shell", "-c", cmd])

# exit with non-zero if not validated
sys.exit(1)
