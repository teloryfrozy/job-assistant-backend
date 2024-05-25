FROM python:3.11

# Install cron
RUN apt-get update && apt-get install -y cron

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
# COPY . .

# Copy the entrypoint script and set it as the entrypoint
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["entrypoint.sh"]

# Expose the port the app runs on
EXPOSE 9000

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9000"]