# Use an official Python image (Ensure Python 3.9+ is used)
FROM python:3.9

# Set the working directory in the container
WORKDIR /dataworks-automation

# Copy the project files into the container
COPY . .

# Update package lists and install SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Upgrade pip to avoid version conflicts
RUN pip install --upgrade pip

# Install dependencies from requirements.txt (Ensure sqlite3 is NOT in the list)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
