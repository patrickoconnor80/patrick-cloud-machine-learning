# File name: Dockerfile
FROM rayproject/ray-ml:2.21.0-cpu

# Set the working dir for the container to /serve_app
WORKDIR /serve

# Copies the local serve files into the WORKDIR
COPY src/serve /serve/