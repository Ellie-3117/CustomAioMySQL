from customaiomysql import Database
import asyncio
async def testhelp():
    m=Database()
    await m.help()
#asyncio.run(testhelp())
async def test_connected():
    m=Database()
    await m.connected(db='setup',file_name='config.cfg')
asyncio.run(test_connected())