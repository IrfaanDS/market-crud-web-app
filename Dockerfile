# Stage 1: Base Image
# Use a Python base image suitable for a web application
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Stage 2: Install Dependencies
# Copy only the requirements file first to take advantage of Docker cache
COPY requirements.txt .

# Install application dependencies
# The --no-cache-dir flag is for smaller image size
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Copy Application Code
# Copy the rest of the application code into the container
COPY . .

# Stage 4: Network Configuration
# Expose the port your Flask app is configured to run on (Flask default is 5000)
EXPOSE 5000

# Stage 5: Execution Command
# Set the command to run the application when the container starts
# CRITICAL: Ensure 'run.py' is the file that launches your Flask application
CMD ["python", "run.py"]