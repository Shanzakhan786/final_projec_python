import os
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())


def get_llm_response(query: str, context: str) -> str:
    """
    Sends a query and context to the Google Gemini LLM and returns the response.
    Args:
        query (str): The user's query to be answered based on the context.
        context (str): Background information delimited by triple backticks.

    Returns:
        str: The response from the LLM.

    Raises:
        ValueError: If the GEMINI_API_KEY is not set in the environment variables.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError(
            "GEMINI_API_KEY is not set in the environment variables. "
            "Please set it to your Google Gemini API key (get key from https://aistudio.google.com/apis/credentials)"
        )

    # Configure the Gemini API key
    genai.configure(api_key=gemini_api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = (
        "You are a helpful assistant that answers questions based on the provided context. "
        "with the context delimited by triple backticks.\n\n"
        "You will be given a context and a query. Your task is to answer the query based on the context. "
        "If you use information to answer the query, you should indicate the source of the information in your response. "
        "If the content is empty or not relevant to the query, you should say 'I don't know'.\n\n"
        "You should always respond in a friendly and helpful tone.\n\n"
        "Personal information should not be included in the response.\n\n"
        f"Context:\n```{context}```\n\n"
        f"Query: {query}"
    )

    response = model.generate_content(prompt)
    return response.text