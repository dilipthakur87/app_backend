# Base image
FROM python:3.12-slim
USER root
# Set work directory
WORKDIR /app

# Copy the requirements file


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# USER appuser
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser
# Set environment variables
ENV FLASK_APP=app.api:app
ENV FLASK_ENV=development

# Expose the Flask port
EXPOSE 5500
RUN flask db upgrade

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5500"]
