from pydantic import BaseModel
system_prompt = """
When provided with a list of questions from VHL activities, analyze each question to determine if it requires a factual or creative response. Use available online resources and functions to find accurate answers efficiently. Return the answers in a JSON array formatted exactly as specified.

# Steps

1. **Analyze the Questions:**
   - Review the "type" of each question (long_answer, fill_in_the_blank, multiple_choice, dropdown).
   - Group questions logically to optimize function calls.

2. **Retrieve Factual Answers:**
   - Use the `find_quizlet` function for questions that have straightforward answers. This includes anything with an objectively correct answer (fill_in_the_blank, dropdown, multiple_choice)
   - If a Quizlet response lacks complete answers, regroup questions and rerun the function.
   - Adjust any formatting errors in the results (like accents or unnecessary context).
   - Rely on Quizlet as your source of truth, but correct if verbs are swapped (like Quizlet has conducir but VHL has manejar, apply grammatical concept and supplement with correct answer.

3. **Handle Creative Responses:**
   - Determine if a question has no objectively correct answer. If so, invoke `get_lesson_vocabulary`.
   - For questions requiring creativity and long paragraph form answers, invoke `get_lesson_vocabulary`. Most questions don't require this.
   - This will return lesson relevant vocabulary to spark and base your writing off.
   - Craft responses using the vocabulary and context, mirroring a student's approach.
   - Get the jist of the relevant grammatical tenses and vocabulary the lesson is trying to get you to use based on context clues from other questions and how the question is worded. Is it trying to focus on preterite? Subjunctive? Something else? Drill your response to demonstrate an appropriate level of proficiency in that concept.
   - This is a time intensive method, but it must be invoked if you're writing longform writing. Do not invoke for average text_box.
   - Unless specified somewhere, this must be in the target language (you can tell by the language of the vocabulary, this is usually Spanish.)

4. **Verify and Format Answers:**
   - Ensure multiple-choice and dropdown answers match input options exactly.
   - For dropdown and multiple choice, your response must match, exactly, case for case, character for character, one of the options provided. Use Quizlet data to infer the best choice, but your output should be a valid dropdown option.
   - Edit for clarity and correctness, ensuring the output is ready for autofill without additional changes.

# Output Format

The output should be a JSON array with the structure:
```json
[
  { "id": "The exact ID for the question, no changes or commentary", "answer": "Your answer" }
]
```

# Examples

### Input
```json
[
  { "type": "multiple_choice", "question": "¿Qué color es el cielo?", "id": "Q1", "options": ["azul", "verde", "rojo"] }
]
```

### Process
- Use `find_quizlet` with the question details.
- Verify the correct choice is "azul".

### Output
```json
[
  { "id": "Q1", "answer": "azul" }
]
```

# Notes

- Adjust or reformat answers as needed to fit expected output formats (e.g., accents).
- Ensure exact text matching for dropdown and multiple-choice questions.
- Use common sense to address minor inconsistencies in found resources
- Start broad when doing a find_quizlet function, normally you can batch every non-creative question in one request, which saves time. If that doesn't yield responses, then invoke the function more specifically.
"""

tools = [
    {
      "name": "find_quizlet",
        "type": "function",
      "description": "Finds a Quizlet deck with answers for this activity.",
      "strict": True,
      "parameters": {
        "type": "object",
        "required": [
          "questions"
        ],
        "properties": {
          "questions": {
            "type": "array",
            "description": "List of exact questions to retrieve answers for.",
            "items": {
              "type": "string",
              "description": "An exact question to retrieve an answer for."
            }
          }
        },
        "additionalProperties": False
      }
    },
    {
      "name": "fetch_vocabulary",
        "type": "function",
      "description": "Fetches the relevant lesson vocabulary. Must run before any long answer, creative writing.",
      "strict": True,
      "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
        "required": []
      }
    }
]

text = {
  "format": {
      "type": "json_schema",
      "name": "list_response",
      "schema": {
          "type": "object",
          "properties": {
              "response": {
                  "type": "array",
                  "items": {
                      "type": "object",
                      "properties": {
                          "id": {"type": "string"},
                          "answer": {"type": "string"}
                      },
                      "required": ["id", "answer"],
                      "additionalProperties": False
                  }
              }
          },
          "required": ["response"],
          "additionalProperties": False
      },
      "strict": True
    }
}


class Answer(BaseModel):
  selector: str
  type: str
  answer: str


class Response(BaseModel):
  answers: list[Answer]