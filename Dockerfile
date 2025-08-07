# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Avoid buffering (important for logs from Gradio etc.)
ENV PYTHONUNBUFFERED=1

# Ensure our shell script is executable
RUN chmod +x entrypoint.sh

# Expose required ports
EXPOSE 8501
EXPOSE 8000
EXPOSE 7860

# Run apps via entrypoint script
CMD ["./entrypoint.sh"]
