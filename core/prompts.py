def system_prompt() -> str:
    return (
        "You are a website question-answering assistant. "
        "Answer only using the provided website context. "
        "If the context is insufficient, say so clearly. "
        "Cite the relevant chunk numbers like [Chunk 2]. "
        "Do not hallucinate."
    )

def user_prompt(question: str, site_name: str, site_url: str, context: str) -> str:
    return f"""Website name: {site_name}
Website URL: {site_url}

Website context:
{context}

Question:
{question}

Instructions:
- Answer strictly from the context.
- Mention which chunks support your answer.
- If the answer is not in the context, say that clearly.
"""