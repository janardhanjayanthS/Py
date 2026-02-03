FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY /src ./src/

EXPOSE 5000

ENV sample=hi_da
ENV host=0.0.0.0
ENV port=5000

CMD ["python", "-m", "src.main"]
