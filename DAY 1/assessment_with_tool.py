"""Ask the same questions with the single course-fee lookup tool available."""
import json

from config import MODEL, banner, client
from assessment_no_tool import ASSESSMENT_QUESTIONS
from assessment_tool import TOOL, get_course_fee


SYSTEM_PROMPT = (
    "You are a college assistant. For every question asking for a college course fee, "
    "call get_course_fee and base your answer on its result. For other questions, "
    "answer directly without using the tool. Do not guess course fees."
)


def ask_with_tool(question: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=[TOOL],
        tool_choice="auto",
        temperature=0,
    )
    message = response.choices[0].message
    if not message.tool_calls:
        return f"Tool call: none\nA: {(message.content or '').strip()}"

    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments or "{}")
    result = get_course_fee(**arguments)
    print(f"Tool call: {tool_call.function.name}({arguments}) -> {result}")

    messages.extend([
        {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
            ],
        },
        {"role": "tool", "tool_call_id": tool_call.id, "content": result},
    ])
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )
    answer = (final_response.choices[0].message.content or "").strip()
    return f"A: {answer}"


if __name__ == "__main__":
    banner("DAY 1 ASSESSMENT: LLM WITH ONE TOOL")
    for question in ASSESSMENT_QUESTIONS:
        print(f"Q: {question}")
        print(ask_with_tool(question))
        print("-" * 72)