# Use the Python 3.10.11 base image
FROM python:3.10.11

# Set the working directory within the container
WORKDIR /testplan-to-mr

# Copy the requirements.txt file from the host to the container
COPY requirements.txt ./requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the testplan-to-mr.py script from the host to the container
COPY testplan-to-mr.py ./testplan-to-mr.py

# Define the command to run when the container starts
CMD [ "python", "./testplan-to-mr.py" ]