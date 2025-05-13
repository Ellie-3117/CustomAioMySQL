# CustomAioMysql

**CustomAioMysql** là một module tuỳ chỉnh dựa trên `aiomysql`, được thiết kế để hoạt động tương tự như `sqlite3`, giúp đơn giản hóa việc sử dụng MySQL bất đồng bộ trong các dự án Python.

## 🚀 Cài đặt

Trước tiên, hãy cài đặt các gói cần thiết:

```sh
pip install aiomysql customtkinter
```

> ✅ Module cũng tự động kiểm tra và cài đặt `aiohttp`, `aiomysql`,  nếu thiếu.

## 📌 Tính năng

- **Giao diện giống sqlite3**: Sử dụng hàm như `execute`, `fetchone`, `fetchall`, `connect` quen thuộc.
- **Hỗ trợ asyncio**: Tận dụng sức mạnh của `aiomysql` để truy vấn không đồng bộ.
- **Lưu thông tin cấu hình**: Tự động lưu và tải lại thông tin kết nối database qua file config.
- **Tự động kiểm tra kết nối mạng** khi kết nối đến host không phải `localhost`.
- **Ghi log** chi tiết cho tất cả truy vấn vào `DatabaseLogging.txt`.

## 🔧 Cách sử dụng

```python
import asyncio
import msql

async def main():
    db = await msql.connect(
        host="localhost",
        port=3306,
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

Hoặc nếu bạn đã lưu cấu hình bằng `connect`, bạn có thể kết nối lại dễ dàng bằng:

```python
await db.connected("test_db")
```

## 📜 API Reference

- `msql.connect(host, port, user, password, database, ...)`  
  Kết nối đến một database và lưu lại cấu hình (`Config/configdb.cfg`).

- `msql.connected(db_name)`  
  Kết nối lại tới database dựa trên file cấu hình đã lưu.

- `db.execute(query: str, params: tuple = None)`  
  Thực thi truy vấn như `INSERT`, `UPDATE`, `DELETE`. Trả về số dòng bị ảnh hưởng.

- `db.fetchall(query: str, params: tuple = None)`  
  Truy vấn và trả về toàn bộ kết quả (danh sách dòng).

- `db.fetchone(query: str, params: tuple = None)`  
  Truy vấn và trả về một dòng duy nhất.

- `db.close()`  
  Đóng kết nối database.

## 📂 Ghi chú cấu hình

File config được lưu tại: `Config/configdb.cfg`  
Với định dạng:

```ini
[database]
host = localhost
port = 3306
user = root
password = your_password
```

> ⚠️ Đảm bảo đường dẫn `Config/` tồn tại hoặc module sẽ tự tạo nếu chưa có.

## 🐞 Ghi log

Mọi truy vấn đều được ghi log vào file `DatabaseLogging.txt`, bao gồm:

- Query thực thi
- Tham số truyền vào
- Số dòng bị ảnh hưởng hoặc kết quả trả về
- Lỗi nếu có

## 📄 Giấy phép

Dự án này được phát hành theo giấy phép **MIT**.  
Bạn có thể tự do chỉnh sửa, phân phối và sử dụng theo ý muốn 💕

---

✨ Nếu bạn thấy dự án hữu ích, hãy ⭐ cho repo này nhé! Mọi góp ý đều được trân trọng 💖
## DEMOCODE
```python
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
```

