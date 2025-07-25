FROM python:3.11.5

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .


CMD uvicorn main:app --host=0.0.0.0 --reload