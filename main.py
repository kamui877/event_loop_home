import concurrent.futures
import asyncio
from aiohttp import ClientSession
from db import Session, CharactersModel
from tqdm.asyncio import tqdm_asyncio


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
TIMEOUT = 30
MAX_WORKERS = 2


async def get_character(char_id: int, session):
    for el in range(1, char_id):
        if el == 17:
            continue
        response = await session.get(f"https://swapi.dev/api/people/{el}", headers=HEADERS, timeout=TIMEOUT)
        characters = await response.json()
        yield characters


async def add_bd_characters(characters: dict):
    character = {"birth_year": characters["birth_year"],
                 "eye_color": characters["eye_color"],
                 "gender": characters["gender"],
                 "hair_color": characters["hair_color"],
                 "height": characters["height"],
                 "homeworld": characters["homeworld"],
                 "mass": characters["mass"],
                 "name": characters["name"],
                 "skin_color": characters["skin_color"],
                 "films": str(characters["films"]),
                 "species": str(characters["species"]),
                 "starships": str(characters["starships"]),
                 "vehicles": str(characters["vehicles"])}
    with Session() as session:
        new_character = CharactersModel(**character)
        session.add(new_character)
        session.commit()
    return {"status": "ok"}


async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        session = ClientSession()
        future_to_url = (executor.submit(add_bd_characters, character) async for character in get_character(84, session))
        async for future in tqdm_asyncio(future_to_url, total=82):
            await future.result()
        await session.close()


if __name__ == '__main__':
    asyncio.run(main())
