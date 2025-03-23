# CustomAioMysql

**CustomAioMysql** là một module tùy chỉnh dựa trên `aiomysql`, được thiết kế để hoạt động tương tự như `sqlite3`, giúp đơn giản hóa việc sử dụng MySQL trong các dự án Python.

## 🚀 Cài đặt

Trước tiên, hãy cài đặt các gói cần thiết:

```sh
pip install aiomysql socket customtkinter
```

## 📌 Tính năng

- **Giao diện giống sqlite3**: Custom aiomysql giống sqlite3 để dễ dùng với bất đồng bộ async.
- **Hỗ trợ asyncio**: Tận dụng sức mạnh của `aiomysql` để truy vấn không đồng bộ.
## 🔧 Cách sử dụng

```python
import asyncio
from customaiomysql import Database


async def main():
    db = await Database.connect(
        host="localhost",
        user="root",
        password="password",
        database="test_db"
    )

    await db.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT)")
    await db.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))

    rows = await db.fetchall("SELECT * FROM users")
    print(rows)

    await db.close()


asyncio.run(main())
```
Bạn có thể xem kỹ hơn với định dạng Database.help()
## 📜 Usage

- `Database.connect(...)` - Kết nối tới MySQL.
- `Database.connected()`-Kết nối lại database được cài đặt trong config
- `db.execute(query, params)` - Thực thi truy vấn (INSERT, UPDATE, DELETE).
- `db.fetchone(query, params)` - Lấy một dòng dữ liệu.
- `db.fetchall(query, params)` - Lấy nhiều dòng dữ liệu.
- `db.close()` - Đóng kết nối.

## 📄 Giấy phép

Dự án này được phát hành theo giấy phép **MIT**.

