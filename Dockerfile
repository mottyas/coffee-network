FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

COPY socialnetwork /socialnetwork

WORKDIR /socialnetwork

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
