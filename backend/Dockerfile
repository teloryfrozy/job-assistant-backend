FROM python:3.11

# Set environment variables
RUN apt-get update && apt-get install -y cron
WORKDIR /backend

# Dependencies
COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Start the backend server
ENTRYPOINT ["entrypoint.sh"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]