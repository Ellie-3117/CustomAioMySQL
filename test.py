import msql
import asyncio
async def test():
    database=msql.msql
    await database.connect(
        host="test",
        port=3306,
        user="DieuNguyen",
        password="123123",
        db="db"
    )
    await database.execute('CREATE TABLE IF NOT EXISTS test(test BIGINT,test2 BIGINT)')
    await database.execute('INSERT INTO test(test,test) value(%s,%s)',(1,2))
    rows = await database.fetchall("SELECT * FROM test")
    print(rows)
asyncio.run(test())
