from customaiomysql import Database
import asyncio
async def testhelp():
    m=Database()
    await m.help()
asyncio.run(testhelp())
