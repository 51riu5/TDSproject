FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create /data directory inside the container and copy sample data
RUN mkdir -p /data && cp -r data/* /data/  || true

EXPOSE 8000

CMD ["python", "app.py"]
