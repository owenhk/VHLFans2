import pydantic

from defs import VHLFans, QuizletFlashcard, QuizletDeck


class CachedVocabulary(pydantic.BaseModel):
    english_translation: str
    spanish_word: str


async def fetch_lesson_vocabulary(lesson_name: str, service: VHLFans) -> QuizletDeck:
    """
    Fetch vocabulary associated with a specific lesson from the database.

    This function retrieves a list of vocabulary words for a specified lesson
    name from the database connection provided by the VHLFans service.
    The vocabulary is returned as a list of CachedVocabulary objects, each
    containing the English translation and corresponding Spanish word.

    :param lesson_name: The name of the lesson for which vocabulary should
        be retrieved.
    :type lesson_name: str
    :param service: An instance of VHLFans, which provides the database
        connection to execute the query.
    :type service: VHLFans
    :return: A list of CachedVocabulary objects containing the English
        translation and Spanish word for the specified lesson.
    :rtype: list[CachedVocabulary]
    """
    assert service.con is not None
    async with service.con.acquire() as con:
        results = await con.fetch(
            """
            SELECT english_translation, spanish_word FROM vocabulary WHERE lesson_name = $1
            """, lesson_name
        )
        deck = []
        for flashcard in results:
            deck.append(
                QuizletFlashcard(
                    front=flashcard[0],
                    back=flashcard[1]
                )
            )
    return QuizletDeck(flashcards=deck)


async def upload_lesson_vocabulary(lesson_name: str, deck: QuizletDeck, service: VHLFans):
    assert service.con is not None
    print("Attempting to upload vocab")
    formatted_deck: [CachedVocabulary] = [CachedVocabulary(english_translation = x.front, spanish_word=x.back) for x in deck.flashcards]
    deck = deck.flashcards
    print(deck)
    print(formatted_deck)
    async with service.con.acquire() as con:
        await con.execute("""
        INSERT INTO units (lesson_name) VALUES ($1) ON CONFLICT DO NOTHING;
        """, lesson_name)
        for x in formatted_deck:
            await con.execute("""
            INSERT INTO vocabulary (lesson_name, english_translation, spanish_word) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING;
            """, lesson_name, x.english_translation, x.spanish_word)

async def fetch_cached_deck(deck_id: str, service: VHLFans) -> QuizletDeck:
    assert service.con is not None
    flashcards: [QuizletFlashcard] = []
    async with service.con.acquire() as con:
        results = await con.fetch("""
            SELECT front, back FROM quizlet_cards WHERE deck_id = $1;
        """, deck_id)
        for r in results:
            flashcards.append(
                QuizletFlashcard(
                    front=r[0],
                    back=r[1]
                )
            )
        return QuizletDeck(flashcards=flashcards)

async def upload_cached_deck(deck_id: str, deck: QuizletDeck, service: VHLFans):
    assert service.con is not None
    async with service.con.acquire() as con:
        await con.execute("DELETE FROM quizlet_cards WHERE deck_id = $1;", deck_id)
        await con.execute("""
        INSERT INTO quizlet_deck (deck_id) VALUES ($1) ON CONFLICT DO NOTHING;
        """, deck_id)
        for x in deck.flashcards:
            await con.execute("""
            INSERT INTO quizlet_cards (deck_id, front, back) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING;
            """, deck_id, x.front, x.back)
