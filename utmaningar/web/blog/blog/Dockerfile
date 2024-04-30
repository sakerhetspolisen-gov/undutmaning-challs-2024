FROM python:3.12.1-alpine
WORKDIR /code
COPY . .
EXPOSE 1337
RUN pip install -r requirements.txt
CMD ["/bin/sh", "serve.sh"]
