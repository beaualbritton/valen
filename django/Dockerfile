#pulled from https://www.docker.com/blog/how-to-dockerize-django-app/
FROM python:3.13

#sets working directory for container
RUN mkdir /backend
WORKDIR /backend

#prevents python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

#pip dependencies 
RUN pip install --upgrade pip 
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

#django
COPY backend/ .

EXPOSE 8000

#match http/ssh for proper repo fetching
RUN useradd -m -u 1001 -s /bin/bash git && usermod -aG git www-data && git config --system --add safe.directory '*'

USER www-data

#gunicorn forwards stdout/sterr to logs
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--capture-output", "--enable-stdio-inheritance", "backend.wsgi:application"]
