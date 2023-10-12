FROM python:3.11

WORKDIR /application

RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY app.py ./
COPY ./internal ./internal
COPY ./runner ./runner
COPY ./config.ini.docker /application/config.ini

CMD ["gunicorn", "--bind", ":8080", "--workers", "3", "app:app"]