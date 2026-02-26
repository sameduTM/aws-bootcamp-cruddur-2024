FROM python:3.10-slim-buster

# create and set /backend-flask folder as working directory
WORKDIR /backend-flask

# Copy file from host to docker container
COPY requirements.txt requirements.txt

# Install the python libraries used by the app
RUN pip3 install -r requirements.txt

# . means everthing within current directory
COPY . .

# Set environment variables
ENV FLASK_ENV=development
ENV PORT=4567

EXPOSE ${PORT}

# python3 -m flask run --host=0.0.0.0 --port=4567
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]
