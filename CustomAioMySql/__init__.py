from server import Server
import asyncio
from config import ConfigDb
from typing import List,Any,Tuple
class CustomAioMySql:
    def __init__(self):
        pass
    async def execute(self,query:str,params:Tuple[Any]=()) -> List[Any]:
            return await Server.execute(query,params)
    async def fetchall(self,query:str,params:Tuple[Any]=()) -> List[Any]:
        return await Server.fetchall(query,params)
    async def fetchone(self,query:str,params:Tuple[Any]=()) -> List[Any]:
        return await Server.fetchone(query,params)
    async def connect(self,host:str,port:str,user:str,password:str,db:str):
        await Server.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db
        )
    async def disconnect(self):
        await Server.close()
    async def connected(self,file_path:str,db:str):
        data=await ConfigDb.load_config(file_path)
        await Server.connect(**data,db=db)
    async def create_config(self,file_name,host,port,user,password):
        await ConfigDb.create_config(file_name,host,port,user,password)

