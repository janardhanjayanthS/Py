FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY package ./package

RUN pip3 install --no-cache-dir -r requirements.txt

COPY /src ./src/

EXPOSE 5003

CMD [ "python", "-m", "src.api.main" ]
