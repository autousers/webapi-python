FROM python:3.8.6-slim

ENV SEEKER_SERVER_URL="https://10.103.3.39:8443"
# Download Seeker Agent from the Server
RUN curl -v -k -o /tmp/seeker-agent.zip "${SEEKER_SERVER_URL}/rest/api/latest/installers/agents/binaries/JAVA"
# Extract to /tmp/seeker
RUN mkdir -p /tmp/seeker && unzip -d /tmp/seeker /tmp/seeker-agent.zip

RUN mkdir /code/

COPY . /code/

WORKDIR /code/

RUN pip install -r requirement.txt

EXPOSE 8000

CMD ["gunicorn","--bind","0.0.0.0:8000","webdemo.wsgi"]
