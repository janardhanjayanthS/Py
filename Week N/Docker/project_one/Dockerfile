FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6000

ENV sample=hi_da
ENV host=127.0.0.5
ENV port=6000

CMD ["python", '-m', 'src.main']
