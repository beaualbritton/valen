#pulled from https://www.docker.com/blog/how-to-dockerize-django-app/
FROM python:3.13

#sets working directory for container
RUN mkdir /backend
WORKDIR /backend

#prevents python from buffering stdout and stderr
ENV PYTHONBUFFERED=1

#pip dependencies 
RUN pip install --upgrade pip 
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

#django
COPY backend/ .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
