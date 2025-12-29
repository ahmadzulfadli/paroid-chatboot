FROM python:3.12-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev g++ gfortran openblas-dev
COPY requirements_docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]