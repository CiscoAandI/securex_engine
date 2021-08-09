FROM python:3.9

WORKDIR /engine

# Install system requirements layer
COPY ops/containers/engine/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy files
COPY src/ /engine/src/

# Connect to proper repo
LABEL org.opencontainers.image.source https://github.com/ciscoaandi/securex_engine

ENTRYPOINT ["python", "src/engine.py"]