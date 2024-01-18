FROM python:3.11
# Expose port 5000 for Flask
EXPOSE 5000
# Set the working directory
WORKDIR /app
# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the application code
COPY . .
# Run the population script before starting the Flask application
CMD ["sh", "-c", "python populate.py && flask run --host 0.0.0.0"]
