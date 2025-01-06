FROM python:3.12-bookworm

WORKDIR /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y wget gnupg2 apt-transport-https ca-certificates

# Add Google Chrome repository
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt