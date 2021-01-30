FROM python:3.9-slim-buster

WORKDIR /usr/src/app

COPY ./src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/main.py ./

ENTRYPOINT [ "python", "./main.py" ]