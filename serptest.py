import unittest
import asyncio

import AIEngine
from app import VHLFans, Input
from WebEngine import SERPer
import asyncpg
from FunKit import MusicStreamer
import os
from defs import Question
from AIEngine import agent


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.con = await asyncpg.create_pool(os.getenv("DATABASE_URL"))

    async def asyncTearDown(self):
        await self.con.close()
    async def test_ai_engine(self):
        questions = [
            Question(
                selector="text",
                type="1",
                question="Vi el (1) ___ en Internet."
            ),
            Question(
                selector="text",
                type="2",
                question="Se necesitaban personas para un (2) ___ de editora en una pequeña..."
            ),
            Question(
                selector="text",
                type="3",
                question="...en una pequeña (3) ___ que se encontraba en el centro de la ciudad."
            ),
            Question(
                selector="text",
                type="4",
                question="Preparé mi (4) ___ con mucha atención y lo envié por correo electrónico."
            ),
            Question(
                selector="text",
                type="5",
                question="Esa tarde me llamó la (5) ___, que se llamaba la señora Piñeda."
            ),
            Question(
                selector="text",
                type="6",
                question="Me dijo que el (6) ___ que ofrecían no era demasiado alto..."
            ),
            Question(
                selector="text",
                type="7",
                question="...pero que los (7) ___, como el seguro de salud, eran excelentes."
            ),
            Question(
                selector="text",
                type="8",
                question="Era una buena oportunidad para (8) ___ experiencia."
            ),
            Question(
                selector="text",
                type="9",
                question="Me pidió que fuera a la oficina al día siguiente para hacerme una (9) ___."
            ),
            Question(
                selector="text",
                type="10",
                question="Había otro (10) ___ en la sala de espera cuando llegué."
            ),
            Question(
                selector="text",
                type="11",
                question="Ese día decidí (11) ___ a mi trabajo anterior..."
            ),
            Question(
                selector="text",
                type="12",
                question="...y desde entonces ejerzo la (12) ___ de editora."
            ),
            Question(
                selector="text",
                type="13",
                question="¡He tenido mucho (13) ___!"
            ),
            Question(
                selector="text",
                type="14",
                question="Write a paragraph about what you did last week using relevant lesson vocabulary."
            )
        ]
        o = await agent.start_ai_solver(
            input=Input(
                questions=questions,
                lesson_id="",
                lesson_name="",
                unit="Lección 16"
            ),
            service=VHLFans(con=self.con)
        )
        print(o)
        self.assertIsInstance(o, AIEngine.Response)

    async def test_fetch_song(self):
        song = await MusicStreamer.fetch_song()
        print(song)
        self.assertIsNotNone(song)


if __name__ == '__main__':
    unittest.main()
