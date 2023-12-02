FROM python:3.10-alpine

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev libressl-dev cargo \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

CMD [“python3”, “./main.py”]
