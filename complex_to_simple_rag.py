from fastapi import FastAPI, HTTPException
from typing import List, Dict
import asyncio
import logging

app = FastAPI()
# Placeholder for the OpenAI API key
OPENAI_API_KEY = "your_openai_api_key_here"

async def decompose_complex_question(question: str) -> List[str]:
    system_message = {"role": "system", "content": "Select the best questions that deconstruct the complex question. Aim for comprehensiveness."}
    user_message = {"role": "user", "content": question}
    messages = [system_message, user_message]

    # Simulated response for the purpose of this example, replace with actual API call
    response = {"choices": [{"message": {"content": "Question 1\nQuestion 2\nQuestion 3"}}]}
    decomposed_questions = response['choices'][0]['message']['content'].strip().split('\n')

    return decomposed_questions

async def specific_query(query_text: str) -> Dict[str, str]:
    """
    Queries a GPT model for an answer to a specific question.
    
    Args:
        query_text (str): The question to query the model about.
    
    Returns:
        Dict[str, str]: A dictionary with the question and the model's response.
    """
    try:
        # Use the question as the prompt for the GPT model
        response_text = await get_gpt_response(query_text)
        return {"question": query_text, "answer": response_text}
    except HTTPException as e:
        # In case of an HTTP exception, return an error message instead
        logging.error(f"Error querying GPT model: {e.detail}")
        return {"question": query_text, "answer": "Failed to get response from the GPT model."}

@app.get("/query/{query_text}")
async def query_category(query_text: str):
    simple_questions = await decompose_complex_question(query_text)
    simple_answers_tasks = [specific_query(sq) for sq in simple_questions]
    simple_answers_results = await asyncio.gather(*simple_answers_tasks)
    simple_answers = [{"question": sq, "answer": result['response']} for sq, result in zip(simple_questions, simple_answers_results)]

    final_answer = await aggregate_answers(query_text, simple_answers)

    logging.info(f"Simple questions: {simple_questions}")
    logging.info(f"Simple answers: {simple_answers}")
    logging.info(f"Final answer: {final_answer}")

    return {"response": final_answer}

async def aggregate_answers(complex_question: str, simple_qas: List[Dict[str, str]]):
    # Construct the prompt with the complex question and the Q&A pairs
    qa_text = "\n".join([f"Q: {qa['question']}\nA: {qa['answer']}" for qa in simple_qas])
    prompt = f"Given the following questions and answers, synthesize a comprehensive explanation for: {complex_question}"

    # Simulated aggregation logic for the purpose of this example, replace with actual aggregation logic
    aggregated_answer = "Simulated comprehensive explanation based on the provided Q&A pairs"

    return aggregated_answer


async def get_gpt_response(prompt: str) -> str:
    """
    Fetches a response from a GPT model given a prompt.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "temperature": 0.5,
        "max_tokens": 150,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.openai.com/v1/completions", json=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="GPT model request failed")
    return response.json()["choices"][0]["text"].strip()

# Example usage within an endpoint
@app.get("/gpt_query/{query_text}")
async def gpt_query_endpoint(query_text: str):
    try:
        response_text = await get_gpt_response(query_text)
        return {"response": response_text}
    except HTTPException as e:
        return {"error": str(e.detail)}