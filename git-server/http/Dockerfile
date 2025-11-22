FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# dependencies 
RUN apt-get update && apt-get install -y git nginx fcgiwrap spawn-fcgi

# add www-data to git gorup
RUN useradd -m -u 1001 -s /bin/bash git && usermod -aG git www-data

# add external nginx file to sites available
COPY nginx.conf /etc/nginx/sites-available/git

# creating symlink between sites available/git and sites enabled, removing default
RUN ln -sf /etc/nginx/sites-available/git /etc/nginx/sites-enabled/git && rm -f /etc/nginx/sites-enabled/default

# expose port 80 (http)
EXPOSE 80 

# start cgi & nginx, flag /srv/git/ as 'safe' (git has file permission safety features)
# TODO: consider making this an entry script with python
CMD sh -c "git config --system --add safe.directory '*' && spawn-fcgi -s /var/run/fcgiwrap.socket -u www-data -g www-data /usr/sbin/fcgiwrap && exec nginx -g 'daemon off;'"
