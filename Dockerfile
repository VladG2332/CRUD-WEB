FROM python:3.13

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["gunicorn", "-b", "0.0.0.0:5002", "run:app"]