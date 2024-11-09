# Backend Dockerfile
FROM python:3.11

# Set the current working directory to /code
WORKDIR /code

# Copy the file with the requirements to the /code directory
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the source code into the container
COPY ./src /code/src
COPY ./main.py /code/main.py

# Set the command to use fastapi run, which uses Uvicorn underneath
# CMD ["fastapi", "run", "src/main.py", "--port", "80"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
