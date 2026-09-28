FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create an unprivileged user and group (UID/GID 1000)
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser

# Install only necessary runtime libraries (libpq-dev) and clean apt cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Copy requirements.txt to leverage Docker build cache optimization
COPY requirements.txt /src/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code with correct owner permissions
COPY --chown=appuser:appgroup . /src

# Copy and setup entrypoint script with Windows-safe carriage return handling
COPY --chown=appuser:appgroup entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && sed -i 's/\r$//' /entrypoint.sh

# Run as unprivileged user for security hardening
USER appuser

ENTRYPOINT ["/entrypoint.sh"]
