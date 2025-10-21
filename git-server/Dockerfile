FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# dependencies 
RUN apt-get update && apt-get install -y git nginx fcgiwrap spawn-fcgi

#creating git folder and setting nginx as owner for read/write
RUN mkdir -p /srv/git && chown -R www-data:www-data /srv/git

#add external nginx file to sites available
COPY nginx.conf /etc/nginx/sites-available/git

#creating symlink between sites available/git and sites enabled, removing default
RUN ln -sf /etc/nginx/sites-available/git /etc/nginx/sites-enabled/git && rm -f /etc/nginx/sites-enabled/default

#initializing empty repo, telling git-http-server daemon external calls are acceptable and to receive over http, then giving nginx access to git directory
RUN git init --bare /srv/git/test.git && touch /srv/git/test.git/git-daemon-export-ok && git --git-dir=/srv/git/test.git config http.receivepack true && chown -R www-data:www-data /srv/git

#expose port 80 (http)
EXPOSE 80 

#runs within container rather than at build time, nginx and fcgi spawn in background
#no systemd here so this needs to be manual
#TODO: consider making this an entry script with python
CMD sh -c "spawn-fcgi -s /var/run/fcgiwrap.socket -u www-data -g www-data /usr/sbin/fcgiwrap && exec nginx -g 'daemon off;'"
