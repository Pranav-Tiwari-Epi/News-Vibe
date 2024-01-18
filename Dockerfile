FROM python:3.11
# Expose port 5000 for Flask
EXPOSE 5000
# Set the working directory
WORKDIR /app
# Copy requirements.txt and install dependencies
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Set the entrypoint script as executable
RUN chmod +x entrypoint.sh
# Specify the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
