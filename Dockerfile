FROM --platform=linux/amd64 python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install fastapi "uvicorn[standard]" gunicorn pyOpenSSL
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--bind", "0.0.0.0:443", "--certfile", "/app/fullchain.pem", "--keyfile", "/app/privkey.pem"]
