# Simple Docker HuggingFace Model
This repository contains the code for the article A Simple to Implement End-to-end Project with HuggingFace: Generating a Ready-to-use HuggingFace Model with FastAPI and Docker. 
The project demonstrates how to deploy a sentiment analysis model using HuggingFace, FastAPI, and Docker.

## Project Overview
The main goal of this project is to enable colleagues within a company to use a pre-trained HuggingFace sentiment analysis model without needing to download or implement it from scratch. 
We achieve this by creating an API endpoint using FastAPI and containerizing the application with Docker for easy deployment.

### Step 1: Choosing our HuggingFace Model
1. Install the necessary libraries:
```
pip install transformers
pip install torch  # or pip install tensorflow
```

2. Import and define the model using the pipeline command.
```
from transformers import pipeline
pipe = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
```

3. Test the model.
```
print(pipe("This tutorial is great!"))
# Output: [{'label': 'POSITIVE', 'score': 0.9998689889907837}]
```

4. Define a function to generate a natural language response:
```
def generate_response(prompt: str):
    response = pipe(prompt)
    label = response[0]["label"]
    score = response[0]["score"]
    return f"The '{prompt}' input is {label} with a score of {score}"
```

### Step 2: Write API Endpoint for the Model with FastAPI
1. Install FastAPI and pydantic:
```
pip install fastapi pydantic uvicorn
```

2. Define the FastAPI app:
```
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

pipe = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

app = FastAPI()

class RequestModel(BaseModel):
    input: str

@app.post("/sentiment")
def get_response(request: RequestModel):
    prompt = request.input
    response = pipe(prompt)
    label = response[0]["label"]
    score = response[0]["score"]
    return f"The '{prompt}' input is {label} with a score of {score}"
```

### Step 3: Use Docker to Run Our Model
1. Create a Dockerfile:
```
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /sentiment

# Copy the requirements.txt file into the root
COPY requirements.txt .

# Copy the current directory contents into the container at /app as well
COPY ./app ./app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run main.py when the container launches, as it is contained under the app folder, we define app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Build and run the Docker image:
```
docker build -t sentiment-app .
docker run -p 8000:8000 --name sentiment-app sentiment-app
```

## Installation
To get started with this project, follow these steps:
1. Clone the repository:
```
git clone https://github.com/rfeers/data-science-portfolio.git
cd data-science-portfolio/end-to-end-projects/simple-docker-hf-model

```

2. Create and activate a virtual environment (optional but recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the required packages:
```
pip install -r requirements.txt
```

## Usage
1. Run the FastAPI app locally:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
2. Send a POST request to the API endpoint:
```
curl -X POST "http://127.0.0.1:8000/sentiment" -H "Content-Type: application/json" -d '{"input":"This tutorial is great!"}'
```
