FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# dependencies 
RUN apt-get update && apt-get install -y git openssh-server python3

# create git user & sshd dir
RUN useradd -m -s /bin/bash git && mkdir -p /var/run/sshd

# allow git to access www-data repos
RUN usermod -aG www-data git && mkdir -p /srv/git 

#copying validation script, read write exec for owner, r/w for group/user. root owns scripts, sshd calls it
COPY scripts/validate_ssh.py /usr/local/bin/validate_ssh
RUN chmod 755 /usr/local/bin/validate_ssh && chown root:root /usr/local/bin/validate_ssh

#copy entrypoint, make executable
COPY scripts/entrypoint.py /entrypoint
RUN chmod +x /entrypoint

#sshd config 
COPY scripts/sshd_git.conf /etc/ssh/sshd_git.conf
RUN echo "Include /etc/ssh/sshd_git.conf" >> /etc/ssh/sshd_config

EXPOSE 22

ENTRYPOINT ["/entrypoint"]

