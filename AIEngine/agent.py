from typing import List
from WebEngine import SERPer
from defs import Input, VHLFans
import json
import AIEngine
from pydantic import BaseModel
import asyncio

class AIResponse(BaseModel):
    id: str
    answer: str

class ListResponse(BaseModel):
    response: List[AIResponse]


async def start_ai_solver(input: Input, service: VHLFans) -> AIEngine.Response:
    client = service.ai
    system_prompt = AIEngine.system_prompt
    tools = AIEngine.tools
    chat_history = [
        {"type": "message", "content": str(input.model_dump_json()), "role": "user"}
    ]
    response = await client.responses.create(
        model="gpt-4o",
        tools=tools,
        instructions=system_prompt,
        tool_choice="auto",
        text=AIEngine.text,
        input=chat_history
    )
    output = response.output
    chat_history.extend(output)
    while True:
        print(output)
        tasks = []
        call_info = []

        for call in output:
            if call.type == "function_call":
                if call.name == "find_quizlet":
                    questions = json.loads(call.arguments)["questions"]
                    query = SERPer.Query(
                        activity_name=input.lesson_name,
                        lesson_number=input.lesson_id,
                        questions=questions
                    )
                    tasks.append(SERPer.fetch_quizlet_deck(query, service))
                    call_info.append((call.call_id, call.name))
                elif call.name == "fetch_vocabulary":
                    tasks.append(SERPer.fetch_unit_vocabulary(input.unit, service))
                    call_info.append((call.call_id, call.name))

        # Run all tool functions in parallel
        results = await asyncio.gather(*tasks)

        # Append their outputs to chat_history
        for (call_id, _), result in zip(call_info, results):
            json_output = json.dumps([card.model_dump() for card in result.flashcards])
            chat_history.append({
                "type": "function_call_output",
                "call_id": call_id,
                "output": json_output
            })

        # Continue conversation with updated tool outputs
        continuation = await client.responses.create(
            model="gpt-4o",
            tools=tools,
            instructions=system_prompt,
            tool_choice="auto",
            text=AIEngine.text,
            input=chat_history
        )

        output = continuation.output
        if output[0].type != "function_call":
            break
        chat_history.extend(output)

    # Final model response parsing
    print(output)
    obj = ListResponse.model_validate_json(output[0].content[0].text)

    answers = [
        AIEngine.Answer(selector=q.selector, type=q.type, answer=a.answer)
        for q, a in zip(input.questions, obj.response)
    ]
    print(answers)

    return AIEngine.Response(answers=answers)