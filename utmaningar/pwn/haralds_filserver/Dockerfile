FROM amd64/ubuntu:22.04
RUN apt-get update && apt-get -y dist-upgrade && apt-get install -y lib32z1

WORKDIR /code
COPY run/ .
RUN apt update
RUN apt install -y socat
EXPOSE 3001

ENTRYPOINT ["/bin/sh", "serve.sh"]
