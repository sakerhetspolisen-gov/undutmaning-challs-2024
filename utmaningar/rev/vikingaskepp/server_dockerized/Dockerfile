
FROM python:3.12.1-alpine
WORKDIR /code
COPY . .
RUN pip install uvicorn
RUN pip install fastapi
EXPOSE 8000
CMD ["/bin/sh", "serve.sh"]
