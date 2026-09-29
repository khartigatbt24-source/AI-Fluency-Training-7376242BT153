# Day 3 Lab Observations

## Step counts from Part C

| Question | Steps used | Tools called |
|---|---:|---|
| Merit scholarship total | 2 | `read_webpage`, `calculator` |
| Hostel student total | 3 | `read_webpage`, `calculator` x2 |
| 15% of AI202 | 2 | `read_webpage`, `calculator` |
| Welcome message | 1 | None |

The chosen `max_steps` is 6, approximately twice the longest successful run.

## Failure log from Part D

| Failure | What happened without guards | Cost |
|---|---|---|
| Repeating loop | The missing `fees.html` error was returned repeatedly until the step limit. | 6 LLM calls/tool attempts |
| Unknown tool with `.get()` | The invented tool produced an `Unknown tool` message and the loop continued safely. | One additional tool turn |
| Unknown tool with `[]` | The invented tool raised `KeyError` and terminated the run. | The whole run was lost |
| Context overflow | Removing truncation sends the approximately 357,000-character page to the model; the result depends on provider limits. | Potential context error, delay, or rate-limit cost |

## Behaviour after the fixes

| Failure | Guard that acted | Result |
|---|---|---|
| Repeating loop | Repeat detection | Stops on the third identical call with a clear diagnostic. |
| Unknown tool | Safe registry lookup | Returns an error string instead of crashing. |
| Context overflow | Tool truncation and character budget | Limits each observation and stops if the conversation grows too large. |

## Chosen limits

| Setting | Value | Justification |
|---|---:|---|
| `max_steps` | 6 | Twice the longest normal run in Part C. |
| `MAX_TOOL_CHARS` | 1500 | Leaves room for several observations while preserving normal fee-page content. |
| `CHAR_BUDGET` | 30000 | Allows a normal run with headroom for model messages. |
| Repeat threshold | 3 | Allows an occasional legitimate repeat before stopping a loop. |

## Discussion answers

1. The loop is the program's responsibility: a failed observation should update control flow, not be retried forever. The fix belongs in the agent loop, where repeated tool calls can be detected.
2. A crash loses the answer and any diagnostic context. An error string lets the model recover, explain the problem, or stop cleanly.
3. Truncation can hide information near the end of a page. A production reader could support paging, search, or a second tool call with an offset while keeping each observation bounded.
4. Proper token counting needs the selected model's tokenizer. Character counting is only approximate, but it is provider-independent and still prevents unbounded growth.
5. Day 1 could benefit from a step limit and safe tool lookup. Repeat detection, truncation, and budget limits become especially important when tools read external or user-controlled content.

## Result

The experiment shows that tool use makes an agent flexible, but the execution loop must enforce bounded retries, bounded observations, and bounded conversation size for reliable behaviour.