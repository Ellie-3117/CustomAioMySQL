# aiomysql_server

`aiomysql_server` là một thư viện Python dùng để hỗ trợ kết nối và giao tiếp với cơ sở dữ liệu MySQL một cách bất đồng bộ.

## Cài đặt

```bash
pip install aiomysql_server
```

## Sử dụng

```python
from Server.custom_aiomysql import CustomAioMySql

async def main():
    mysql = CustomAioMySql()
    await mysql.connect(host="localhost", port="3306", user="root", password="password", db="test_db")
    result = await mysql.fetchall("SELECT * FROM users")
    print(result)
    await mysql.disconnect()
```

Xem thêm tại [tài liệu](https://github.com/your_github/aiomysql_server).