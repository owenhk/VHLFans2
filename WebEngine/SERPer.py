import aiohttp
from defs import VHLFans, QuizletDeck, QuizletFlashcard
from CacheEngine import uploadtocache
import pydantic
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Query(pydantic.BaseModel):
    activity_name: str
    lesson_number: str
    questions: list[str]


async def fetch_quizlet_deck(query: Query, service: VHLFans) -> QuizletDeck:
    async with aiohttp.ClientSession(connector=service.tcp_connector) as session:
        questions_formatted_as_string = " ".join(query.questions)
        params = {
            "q": "site:quizlet.com " + f" VHL {query.activity_name} {query.lesson_number} {questions_formatted_as_string}"
        }
        headers = {
            "X-API-Key": service.serp_api_key,
            "Content-Type": "application/json"
        }
        async with session.post("https://google.serper.dev/search", params=params, headers=headers) as r:
            results = await r.json()
            print(results)

    top_score = 0
    cached_result = None
    for result in results["organic"]:
        # First, check if this deck exists in the cache
        parsed = urlparse(result["link"])
        deck_id = parsed.path.strip("/").split("/")[0]
        cached_deck = await uploadtocache.fetch_cached_deck(deck_id, service)
        used_cache = False
        if len(cached_deck.flashcards) == 0:
            cards = await QuizletScrape(result["link"], service)
        else:
            used_cache = True
            cards = cached_deck
        ai_list = []
        for card in cards.flashcards:
            ai_list.append(f"Front of card: '{card.front}', Back of card: '{card.back}'")
        messages = [
            {
                "role": "system",
                "content": "Your job is to score the following Quizlet flashcard deck for its usefullness to answer the lesson questions. AI will be matching them later, so if it has too much content or it's out of order, it **doesn't** matter."
                           " Your score, out of 10, is entirely reflectant on the flashcards ability to answer the questions in the lesson."
                           " A score of 1 means the deck is useless, it answers no questions, 10 means it contains the answers to all questions in the lesson, and anything in between means it gets close. Remember, too many answers, the order, or how it's laid out, doesn't matter."
                           " Your response must only contain a number, between 1 and 10, written as an integer without any text or explanation."
            },
            {
                "role": "user",
                "content": "Questions the deck needs to answer:" + f"""
                '''
                {"\n".join(query.questions)}
                ```
                """
            },
            {
                "role": "user",
                "content": f"""
                Here are the cards in this deck:
                {ai_list}
                """
            }
        ]
        completion = await service.ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2
        )
        score = completion.choices[0].message.content
        score = int(score)
        if score > 8:
            if not used_cache:
                await uploadtocache.upload_cached_deck(deck_id, cards, service)
            return cards
        else:
            if score > top_score:
                top_score = score
                cached_result = cards
    return cached_result if cached_result else None

async def QuizletScrape(url: str, service: VHLFans) -> QuizletDeck:
    quizlet = await fetch_web_html(url, service)
    soup = BeautifulSoup(quizlet, 'html.parser')

    flashcards = []

    term_divs = soup.find_all("div", class_="SetPageTermsList-term")
    for term in term_divs:
        # Each flashcard has two sides identified by the data-testid attribute
        sides = term.find_all("div", attrs={"data-testid": "set-page-term-card-side"})
        if len(sides) >= 2:
            # The first side is considered the front and the second side the back
            front = sides[0].get_text(separator=" ", strip=True)
            back = sides[1].get_text(separator=" ", strip=True)
            flashcards.append(QuizletFlashcard(front=front, back=back))

    return QuizletDeck(flashcards=flashcards)

async def fetch_unit_vocabulary(unit: str, service: VHLFans) -> QuizletDeck:
    results = await uploadtocache.fetch_lesson_vocabulary(unit, service)
    if len(results.flashcards) > 0:
        return results
    async with aiohttp.ClientSession(connector=service.tcp_connector) as session:
        params = {
            "q": f"site:quizlet.com {unit} VHL Vocabulary"
        }
        headers = {
            "X-API-Key": service.serp_api_key,
            "Content-Type": "application/json"
        }
        async with session.post("https://google.serper.dev/search", params=params, headers=headers) as r:
            results = await r.json()
            result = results["organic"][0]
            cards = await QuizletScrape(result["link"], service)
            await uploadtocache.upload_lesson_vocabulary(unit, cards, service)
            return cards

async def fetch_web_html(url: str, service: VHLFans) -> str:
    async with aiohttp.ClientSession(connector=service.tcp_connector) as session:
        payload = {
            "api_key": service.serp_api_key,
            "url": url,
            "render": 'true'
        }
        async with session.get("https://api.scraperapi.com/", params=payload) as r:
            text = await r.text()
            return text