FROM python:3.9.19-alpine3.19

# Create and set the working directory to /app
WORKDIR /app

# Copy the application files to the container
COPY ./flaskpost /app/flaskpost
COPY run.py /app

# Install the required python packages listed in the requirements file
# Ensure that your requirements.txt file is in the flaskpost directory or adjust the path accordingly
COPY ./flaskpost/requirements.txt /app
RUN python3 -m pip install -r requirements.txt

# Set environment variable to point to the Flask app
ENV FLASK_APP run.py

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
