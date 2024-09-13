FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["bash", "-c", "entrypoint.sh"]
