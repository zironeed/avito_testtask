FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

EXPOSE 8080

CMD ["/bin/bash", "/app/entrypoint.sh"]
