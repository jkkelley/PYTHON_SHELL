# Use a lightweight Python base image
FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY . .

# Set python as the entrypoint so any script can be passed as an argument
ENTRYPOINT ["python"]

# Default file to run if no argument is provided
CMD ["decode.py"]


# podman run --rm --entrypoint "python" secret-decoder \
# codex_decode.py "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"