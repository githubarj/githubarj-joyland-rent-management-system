FROM jenkins/jenkins:lts
USER root
RUN apt-get update && apt-get install -y docker.io && \
    mkdir -p /usr/local/lib/docker/cli-plugins && \
    curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-aarch64 \
    -o /usr/local/lib/docker/cli-plugins/docker-compose && \
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
USER jenkins
