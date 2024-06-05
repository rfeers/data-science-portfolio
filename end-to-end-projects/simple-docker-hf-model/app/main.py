from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# You can check any other model in the Hugging Face Hub. In my case I chose this one to classify text by positive and negative sentiment. 
pipe = pipeline(model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

# We define the app
app = FastAPI()

# We define that we expect our input to be a string
class RequestModel(BaseModel):
    input: str

# Now we define that we accept post requests
# ->  In APIs, requests are made to ask the API to perform a certain task — in this case to analyze a piece of text. 
@app.post("/sentiment")
def get_response(request: RequestModel):
    # We get the input prompt
    prompt = request.input

    # We use the hf model to classify the prompt
    response = pipe(prompt)

    # We get both the label and the score from the input
    label = response[0]["label"]
    score = response[0]["score"]
    return f"The '{prompt}' input is {label} with a score of {score}"
