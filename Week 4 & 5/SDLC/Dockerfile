FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r --no-cahce-dir requirements.txt

COPY . .

EXPOSE 5003

CMD [ "python", "-m", "src.api.main" ]
