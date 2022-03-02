FROM python:3.8.6-slim as webapp
RUN mkdir /code/
COPY . /code/
WORKDIR /code/
RUN pip install -r requirement.txt
EXPOSE 8000
CMD ["gunicorn","--bind","0.0.0.0:8000","webdemo.wsgi"]
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
