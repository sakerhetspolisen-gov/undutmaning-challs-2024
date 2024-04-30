FROM python:3.12.1-alpine
WORKDIR /code
COPY . .
RUN apk add --no-cache openssh-keygen
RUN mkdir -p /etc/ssh/
RUN ssh-keygen -q -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
RUN pip install prompt_toolkit==3.0.43
RUN pip install asyncssh
EXPOSE 22
CMD ["/bin/sh", "serve.sh"]
