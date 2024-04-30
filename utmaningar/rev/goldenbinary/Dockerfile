FROM debian:latest

ENV DEBIAN_FRONTED noninteractive

RUN apt-get update --fix-missing && apt-get -qy upgrade && apt-get install -y build-essential

WORKDIR /code

CMD /bin/bash -c 'mkdir -p build && gcc -o build/golden src/fibb.c -lm && gcc -o build/flag-bin src/flag.c && build/golden build/flag-bin build/flag && rm build/flag-bin && strip build/golden'
