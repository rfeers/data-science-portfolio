## Code to send a request to the seniment model API end-point. 

import requests

# Define the input data
input_data = {
    "input": "I love this product!"
}

# Send a POST request to the FastAPI endpoint
response = requests.post("http://0.0.0.0:8000/sentiment", json=input_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the response data
    response_data = response.text
    
    # Print the results
    print(response_data)
else:
    print("Error:", response.text)