FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5003

CMD [ "python", "-m", "src.api.main" ]
