# Use official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.yml /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.yml
# Copy the rest of the application files
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
