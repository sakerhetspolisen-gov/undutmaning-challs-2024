
FROM python:3.12.1
WORKDIR /code
COPY . .
RUN apt update
RUN apt install -y socat
EXPOSE 3000
WORKDIR /code/src/
CMD ["/bin/sh", "serve.sh"]
