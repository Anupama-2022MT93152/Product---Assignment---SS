# Use a base image with the appropriate Python version and other dependencies
FROM python:3.12

# Set the working directory within the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

RUN pip install --upgrade pip
# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client
# Install application dependencies (if not already included in your project)
RUN pip install -r requirements.txt

# Expose any necessary ports (if your application listens on a specific port)
ENV LISTEN_PORT=5001
EXPOSE 5001

# Define the command to run your application
CMD ["python", "product.py"]