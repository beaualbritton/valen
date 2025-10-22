FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

# dependencies 
RUN apt-get update && apt-get install -y git nginx fcgiwrap spawn-fcgi

#add external nginx file to sites available
COPY nginx.conf /etc/nginx/sites-available/git

#creating symlink between sites available/git and sites enabled, removing default
RUN ln -sf /etc/nginx/sites-available/git /etc/nginx/sites-enabled/git && rm -f /etc/nginx/sites-enabled/default

#expose port 80 (http)
EXPOSE 80 

#runs within container rather than at build time, nginx and fcgi spawn in background
#no systemd here so this needs to be manual
#TODO: consider making this an entry script with python
CMD sh -c "chown -R www-data:www-data /srv/git && spawn-fcgi -s /var/run/fcgiwrap.socket -u www-data -g www-data /usr/sbin/fcgiwrap && exec nginx -g 'daemon off;'"
