# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 8080

# Set environment variable to allow Flask to run in any environment
ENV FLASK_ENV=production

# Start the app using gunicorn (recommended for production)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
