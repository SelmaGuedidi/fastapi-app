FROM bitnami/kubectl:latest

USER root

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y python3 python3-venv python3-pip

# Create a virtual environment and install packages
RUN python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install pytest

# Set environment variables for the virtual environment
ENV PATH="/venv/bin:${PATH}"

# Set permissions for the Jenkins workspace directory
RUN mkdir -p /home/jenkins/agent/workspace && \
    chown -R 1001:1001 /home/jenkins/agent/workspace

USER 1001