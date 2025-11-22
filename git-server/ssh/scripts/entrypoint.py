#!/usr/bin/env python3
import subprocess
from pathlib import Path

SRV_GIT = "/srv/git"
HOME_GIT_SSH = "/home/git/.ssh"
AUTH_SRV = f"{SRV_GIT}/.ssh/authorized_keys"
AUTH_HOME = f"{HOME_GIT_SSH}/authorized_keys"

# group permissions for /srv/git
subprocess.run(["chown", "-R", "git:www-data", SRV_GIT])
subprocess.run(["find", SRV_GIT, "-type", "d", "-exec", "chmod", "2775", "{}", "+"])
subprocess.run(["find", SRV_GIT, "-type", "f", "-exec", "chmod", "664", "{}", "+"])

# .ssh server dir
subprocess.run(["mkdir", "-p", HOME_GIT_SSH])
subprocess.run(["chmod", "700", HOME_GIT_SSH])

if Path(AUTH_SRV).exists():
    subprocess.run(["cp", AUTH_SRV, AUTH_HOME])
else:
    subprocess.run(["touch", AUTH_HOME])

# set mode & owner of home to git user
subprocess.run(["chown", "-R", "git:git", HOME_GIT_SSH])
subprocess.run(["chmod", "600", AUTH_HOME])

# start sshd
subprocess.run(["/usr/sbin/sshd", "-D"])
