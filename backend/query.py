from backend.vector_store import vector_db
from backend.prompts import SYSTEM_PROMPT

import ollama


def ask_question(question):

    # SEARCH VECTOR DATABASE
    results = vector_db.similarity_search(
        question,
        k=2
    )

    # CREATE CONTEXT
    context = ""

    for doc in results:
        context += doc.page_content + "\n"

    # FINAL PROMPT
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    # OLLAMA RESPONSE
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']