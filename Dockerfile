FROM python:3.8.6-slim

RUN mkdir /code/

COPY . /code/

WORKDIR /code/

RUN pip install -r requirement.txt

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","webdemo.wsgi"]
