import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='postgres', password='1234',
                                 database='postgres', host='127.0.0.1')
    values = await conn.fetch(
        "SELECT * FROM cars where model='d2'"
    )
    print(values)
    await conn.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

