# Complex-to-Simple-RAG

FastAPI GPT Integration
This FastAPI application demonstrates how to decompose complex questions into simpler ones, query specific information, aggregate the answers into a comprehensive response, and directly query a GPT model for a response to a given text input.

Features
Complex Question Decomposition: Break down complex questions into simpler, more manageable queries.
Specific Information Querying: Fetch specific answers based on decomposed questions.
Answer Aggregation: Combine answers to simple queries into a comprehensive response to the original complex question.
Direct GPT Model Querying: Directly send queries to a GPT model and receive responses.
Installation
Ensure you have Python 3.7+ installed on your system. Then, follow these steps to set up the application:

Clone the repository:

bash
Copy code
git clone <repository-url>
cd <repository-directory>
Install the required dependencies:

Copy code
pip install fastapi uvicorn httpx
Set up your OpenAI API key:

Obtain an API key from OpenAI.
Replace "your_openai_api_key_here" in the application code with your actual API key.
Running the Application
Start the FastAPI server:

css
Copy code
uvicorn main:app --reload
Replace main with the name of your Python file if it's different.

The server will start at http://127.0.0.1:8000. You can access the API documentation at http://127.0.0.1:8000/docs.

Usage
Query Decomposition and Aggregation
Endpoint: /query/{query_text}
Method: GET
Description: Decomposes a complex question, queries for answers to the simpler questions, and aggregates the answers.
Direct GPT Model Query
Endpoint: /gpt_query/{query_text}
Method: GET
Description: Sends a query text directly to a GPT model and retrieves the response.
Example Request
Using curl to send a direct GPT model query:

rust
Copy code
curl -X 'GET' \
  'http://127.0.0.1:8000/gpt_query/What%20is%20the%20capital%20of%20France?' \
  -H 'accept: application/json'
