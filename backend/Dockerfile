FROM python:3.11

RUN apt-get update && apt-get install -y cron

WORKDIR /backend

COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]