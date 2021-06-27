# syntax=docker/dockerfile:1

FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

WORKDIR /app/aimpathy

RUN python setup.py sdist bdist_wheel && \
    pip3 install -e .

WORKDIR /app/api

# EXPOSE 80

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]