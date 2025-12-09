# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define the entrypoint for the container
ENTRYPOINT ["python", "inference.py"]

# Set a default command to run inference on the sample audio file
CMD ["--audio-file", "sample_audio.wav"]
