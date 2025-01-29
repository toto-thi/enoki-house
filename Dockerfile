# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the simulation script into the container
COPY simulate_data.py .

# Install the required Python libraries
RUN pip install --upgrade --no-cache-dir paho-mqtt

# Run the simulation script
CMD ["python", "simulate_data.py"]