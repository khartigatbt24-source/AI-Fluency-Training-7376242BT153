# From Prompt to Action: Course-Fee Assistant

## Scenario

This assessment uses the course-fee scenario already present in the project. The college's current fee data is private application data: CS101 costs Rs. 12,000, AI202 costs Rs. 18,000, and DS303 costs Rs. 15,000. The examples below compare the same configured language model answering directly with answering when it can use one course-fee lookup function. A welcoming message is included as a question that does not need the private data.

## Concepts in the Scenario

A Large Language Model (LLM) is a model trained to generate text from patterns learned from its training data and the conversation it receives. It can usually write a suitable welcome message because that is a general language task. It cannot know this college's current private fee table merely because it is asked. Without being given the data or a way to retrieve it, a fee answer may be a guess that sounds certain. The fact that an answer is fluent does not make it verified.

An LLM agent is an LLM connected to software that can take actions on its behalf. For the question “What is the current tuition fee for AI202?”, a plain chat response is generated immediately from the prompt and model knowledge. The tool-enabled assistant can first decide that the private fee is missing, request a lookup, receive the college's value, and then formulate its answer from that result. For the welcome-message question, it can answer directly because no lookup is needed.

A tool is a program function that performs a defined operation outside the model, here looking up one course code in the college's fee table. A tool call is the model's structured request to run that function. The schema tells the model the tool's name, what it does, and which argument it requires. Without a useful description and parameter definition, the model cannot reliably tell when the tool applies or what input format to provide.

For the AI202 fee question, the flow is: the user asks for the current fee; the application sends the question and tool schema to the model; the model selects `get_course_fee` and supplies `{"course_code":"AI202"}`; the application runs the function against the college's data and gets `AI202: Rs. 18,000`; the application returns that result to the model as a tool message; and the model gives a natural-language answer based on the returned value. The printed trace makes the tool request and result visible.

Tools should return readable text for both success and failure. If a course code is unknown, a message such as “Unknown course code: XYZ999” can be sent back to the model, which may explain the problem or ask for clarification. An uncaught exception can stop the whole script before the model can recover or provide a useful answer.

## Comparison

| Basis for comparison | Plain LLM prompt (no tool) | LLM with one tool |
|---|---|---|
| Source of the answer | The model's trained knowledge and prompt context. | The fee lookup's college data, followed by the model's explanation. |
| Can it fetch or compute information outside its own memory? | No. It only generates text from what is in the prompt and its learned patterns. | Yes. It can request the fee lookup function for a course code. |
| Reliability on factual or numeric questions | Unreliable for private or changing college fees; it may guess. | Reliable for known course codes when the lookup data is current and the function runs correctly. |
| Transparency | There is no external source or operation to inspect. | The function name, arguments, and returned fee can be logged and checked. |
| Speed / cost of getting an answer | Usually one model request; fast and lower cost for a simple response. | A lookup question usually needs a model request, function execution, and a follow-up model request; this adds some latency and cost. |

## Minimal Implementation

The implementation is deliberately limited to one external function: `get_course_fee(course_code)`, in `assessment_tool.py`. `assessment_no_tool.py` sends three questions to the model without a tool schema. `assessment_with_tool.py` sends those same questions with the single fee lookup schema available, executes any requested lookup, sends its result back to the model, and prints both the call and final answer. The fee data comes from the existing `COURSE_FEES` mapping in `config.py`.

## Observations

The following questions were run by both scripts with Groq's `openai/gpt-oss-120b` model, so the comparison uses the same prompts and provider:

| Question | Plain LLM observation | Tool-enabled observation |
|---|---|---|
| What is the current tuition fee for course AI202 at our college? | The model declined to provide a current amount and directed the user to the college or registrar. It did not guess. | It called `get_course_fee` with `AI202`, received Rs. 18,000, and stated that fee in its answer. |
| Write a warm one-sentence welcome for a new AI student. | It produced a suitable welcoming sentence without needing private data. | It made no tool call and produced a suitable welcoming sentence directly. |
| What is the current tuition fee for course CS101 at our college? | The model declined to provide the fee and suggested checking the college website or registrar. It did not guess. | It called `get_course_fee` with `CS101`, received Rs. 12,000, and used that amount in its answer. |

The terminal outputs from both runs are saved as screenshots in `screenshots/`. The fee lookup's returned values can be checked independently against `config.py`; model wording may vary by provider and model.

## Suitability and Conclusion

In this scenario, a plain prompt is sufficient for composing a welcome message because the task depends on general language ability, not current college records. A tool becomes necessary when the answer depends on private or updated fee data. The lookup changes the source of the key fact from a model-generated guess to an application value that can be inspected.

More generally, a plain LLM prompt is appropriate for drafting, summarizing supplied text, brainstorming, and explaining stable general concepts. A tool is needed when the task depends on current or private information, exact calculations, files or databases not included in the prompt, or an external action such as sending a message. Tools do not guarantee correctness by themselves: their data, schemas, execution, and returned results still need to be designed and checked.