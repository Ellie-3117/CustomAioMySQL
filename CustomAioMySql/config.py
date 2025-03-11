from configparser import ConfigParser
import os
from typing import List
class ConfigDb:
    async def load_config(self,file_name:str):
        config = ConfigParser()
        config.read(file_name)
        host = config.get("database", "host")
        port = config.getint("database", "port", fallback=3306)
        user = config.get("database", "user")
        password = config.get("database", "password")
        if not host or not user or not password:
            raise ValueError("Missing one or more required database configuration fields: host, user, or password.")
        return List[host, port, user, password]
    async def create_config(self,file_name:str,host:str,port:int,user:str,password:str):
        config = ConfigParser()
        config.add_section("database")
        config.set("database", "host", value=host)
        config.set("database", "port", value=port)
        config.set("database", "user",value=user)
        config.set("database", "password", value=password)
        with open(file_name, "w") as configfile:
            config.write(configfile)
