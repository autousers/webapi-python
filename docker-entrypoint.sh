#!/bin/bash
# docker-entrypoint.sh 
### Original Script Configuration – or empty if simple command.
…
### Seeker Configuration
if [[ ! -z ${SEEKER_ENABLED} ]]; then
  rm -rf /var/lib/apt/lists/* && apt-get update && apt-get install curl -y 
  curl -v -k -o seeker-agent.tar "${SEEKER_SERVER_URL}/rest/api/latest/installers/agents/binaries/PYTHON"
  ls -l
  tar -xvzf seeker-agent.tar
fi
### Original Run Command or equivalent (potentially with new Seeker Arguments as required by the application configuration)
### Should include potential CMD arguments provided to Docker if originally a simple command (accomplished here by $*) 

#su webgoat -c "java $SEEKER_COMMAND -Djava.security.egd=file:/dev/./urandom -jar /home/webgoat/webgoat.jar $*"
