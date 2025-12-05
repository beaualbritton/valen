#!/usr/bin/env python3
import subprocess
from pathlib import Path

SRV_GIT = "/srv/git"
HOME_GIT_SSH = "/home/git/.ssh"
SRV_GIT_SSH = "/srv/git/.ssh"
AUTH_SRV = f"{SRV_GIT}/.ssh/authorized_keys"
AUTH_HOME = f"{HOME_GIT_SSH}/authorized_keys"

# group permissions for /srv/git
subprocess.run(["chown", "-R", "git:www-data", SRV_GIT])
subprocess.run(["find", SRV_GIT, "-type", "d", "-exec", "chmod", "2775", "{}", "+"])
subprocess.run(["find", SRV_GIT, "-type", "f", "-exec", "chmod", "664", "{}", "+"])

# .ssh server dir
subprocess.run(["mkdir", "-p", SRV_GIT_SSH])
subprocess.run(["chmod", "770", SRV_GIT_SSH])
subprocess.run(["chown", "git:www-data", SRV_GIT_SSH])

if not Path(AUTH_SRV).exists():
    subprocess.run(["touch", AUTH_SRV])

# set mode & owner of home to git user
subprocess.run(["chown", "git:www-data", AUTH_SRV])
subprocess.run(["chmod", "660", AUTH_SRV])

# synlink for srv/git/.ssh and home/git/.ssh
subprocess.run(["mkdir", "-p", "/home/git"])
subprocess.run(["ln", "-sfn", SRV_GIT_SSH, HOME_GIT_SSH])
subprocess.run(["chown", "-h", "git:git", HOME_GIT_SSH])

# start sshd
subprocess.run(["/usr/sbin/sshd", "-D"])
