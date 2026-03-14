FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt pyproject.toml ./
COPY cyberlab/ ./cyberlab/
COPY labs/ ./labs/

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create entrypoint script
RUN echo '#!/bin/bash\n\
echo "Open Cyber Lab"\n\
echo "==============="\n\
exec python cyberlab.py "$@"\n' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["--help"]
