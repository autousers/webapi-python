FROM python:3.8.6-slim

RUN apt-get update; apt-get install curl unzip -y

RUN mkdir /code/

COPY . /code/

WORKDIR /code/

RUN pip install -r requirement.txt

RUN pip install --trusted-host 10.103.3.39 --extra-index-url "https://10.103.3.39:8443/pypi-server/simple" seeker-agent

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","webdemo.wsgi"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
