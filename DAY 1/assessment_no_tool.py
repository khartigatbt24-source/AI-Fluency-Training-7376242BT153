"""Ask the assessment questions directly, without giving the LLM a tool."""
from config import MODEL, QUESTIONS, banner, client


ASSESSMENT_QUESTIONS = [
    "What is the current tuition fee for course AI202 at our college?",
    "Write a warm one-sentence welcome for a new AI student.",
    "What is the current tuition fee for course CS101 at our college?",
]


def ask_without_tool(question: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful college assistant."},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return (response.choices[0].message.content or "").strip()


if __name__ == "__main__":
    banner("DAY 1 ASSESSMENT: PLAIN LLM (NO TOOL)")
    for question in ASSESSMENT_QUESTIONS:
        print(f"Q: {question}")
        print(f"A: {ask_without_tool(question)}")
        print("-" * 72)