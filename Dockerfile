# 1. Base Image:
# Start from a lightweight official Python image.
FROM python:3.9-slim

# 2. Set the Working Directory:
# All subsequent commands will run from this directory inside the container.
WORKDIR /app

# 3. Copy and Install Dependencies:
# First, copy your requirements file into the container.
COPY Requirements.txt /app/
# Upgrade pip and install all required packages.
RUN pip install --upgrade pip && pip install -r Requirements.txt

# 4. Copy Your Application Code:
# This command copies all files from your project into the container.
COPY . /app

# 5. Expose the Port:
# FastAPI will run on port 8000, so expose that port.
EXPOSE 8000

# 6. Command to Run Your Application:
# This starts the FastAPI server using Uvicorn.
CMD ["./entrypoint.sh"]
