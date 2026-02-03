FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY /src .

EXPOSE 5003

ENV POSTGRESQL_PWD=${POSTGRESQL_PWD}}
ENV ENVIRONMENT=${ENVIRONMENT}}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}}
ENV LOG_LEVEL=${LOG_LEVEL}}

CMD [ "python", "-m", "src.api.main" ]
