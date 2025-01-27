FROM python:3.10.6-slim

# Install app
COPY . /usr/app
WORKDIR /usr/app

# Install dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Battlesnake
CMD [ "python", "main.py" ]
