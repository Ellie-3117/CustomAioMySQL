import asyncio,aiomysql,socket
from typing import Optional,Tuple,Any,List
class Server:
    def __init(self,pool:Optional[aiomysql.Pool]=None)->None:
        self.pool=Optional[aiomysql.Pool]=pool
    async def check_internet_connection(self)->str:
        try:
            with socket.create_connection(('google.com',80),80):
                pass
        except:
            return "No Internet Connection"
        return None
    async def connect(self,
            host:str,
            port:int,
            user:str,
            password:str,
            db:str,
            minsize:int=1,
            maxsize:int=10,
            autocommit:bool=True
                      ):
        if host!='localhost':
            connection=await self.check_internet_connection()
            if connection:
                raise ConnectionError(connection)
        try:
            self.pool=await aiomysql.create_pool(host=host,port=port,user=user,password=password,db=db,minsize=minsize,maxsize=maxsize,autocommit=autocommit)
        except Exception as e:
            raise e
        except aiomysql.Error as ae:
            raise ae
    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()
    async def execute(self,query:str,params:Tuple[Any]=None)->List[Tuple[Any]]:
        if not self.pool:
            raise Exception('Database not connected please use connect database with connect or connected')
        try:
            async with self.pool.acquire() as connection:
                con:aiomysql.Connection = connection
                async with con.cursor() as cursor:
                    cur:aiomysql.Cursor = cursor
                    await cur.execute(query,params)
                    if query.strip().upper().startswith('SELECT'):
                        return await cur.fetchall()
                    else:
                        await con.commit()
                        return cur.rowcount
        except Exception as e:
            raise e
    async def fetchall(self, query: str, params: Optional[Tuple] = None) -> List:
            if not self.pool:
                raise Exception('Database connection is None try to connect database with connect')
            try:
                async with self.pool.acquire() as conn:
                    connection: aiomysql.Connection = conn
                    async with connection.cursor() as cur:
                        cursor: aiomysql.Cursor = cur
                        await cursor.execute(query, params)
                        results = await cursor.fetchall()
                        return results
            except Exception as e:
                raise e

    async def fetchone(self, query: str, params: Optional[Tuple] = None) -> List:
        if not self.pool:
            raise Exception('Database connection is None try to connect database with connect')
        try:
            async with self.pool.acquire() as conn:
                connection: aiomysql.Connection = conn
                async with connection.cursor() as cur:
                    cursor: aiomysql.Cursor = cur
                    await cursor.execute(query, params)
                    results = await cursor.fetchone()
                    return results
        except Exception as e:
            raise e




