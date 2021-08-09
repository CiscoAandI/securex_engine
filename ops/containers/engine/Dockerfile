FROM python:3.9

WORKDIR /engine

# Install system requirements layer
COPY ops/containers/engine/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy files
COPY src/ /engine/src/

ENTRYPOINT ["python", "src/engine.py"]