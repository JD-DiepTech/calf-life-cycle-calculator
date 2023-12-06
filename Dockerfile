# Use the official Python base image from Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install git to clone the repository
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/JD-DiepTech/calf-life-cycle-calculator.git .

# Install any necessary dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]