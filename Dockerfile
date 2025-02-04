# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Install manually all the missing libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gconf-service \
    libasound2 \
    libatk1.0-0 \
    libcairo2 \
    libcups2 \
    libfontconfig1 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libxss1 \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

EXPOSE 8002
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--bind", "0.0.0.0:8002", "--config", "gunicorn_config.py", "--timeout", "6000", "app:app"]

