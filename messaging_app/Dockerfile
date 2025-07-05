# Use official Python 3.10 base image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: install MySQL client if using MySQL DB
RUN apt-get update && apt-get install -y default-mysql-client

# Copy project files into the container
COPY . .

# Expose Django default port
EXPOSE 8000

# CMD should include "-p" in the runserver command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
