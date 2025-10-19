# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy frontend code and dependencies
COPY . /app/
COPY india_states.geojson /app/india_states.geojson

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Set Streamlit configuration
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ENABLECORS=false

# Run the dashboard
CMD ["streamlit", "run", "election_dashboard.py"]
