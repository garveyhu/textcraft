# Use the official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the contents of your local directory to the container's working directory
COPY . .

# Make your run.sh script executable (if needed)
RUN chmod +x ./run.sh

# Define the command to run when the container starts
CMD ["./run.sh"]
