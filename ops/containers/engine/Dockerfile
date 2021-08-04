FROM python:3.9

WORKDIR /engine

# Install system requirements layer
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENTRYPOINT ["python", "src/engine.py"]