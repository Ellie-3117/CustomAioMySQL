import customtkinter, asyncio, aiomysql, socket
from typing import Optional, Tuple, Any, List, Dict
from configparser import ConfigParser
from tkinter import messagebox
import tkinter
import sys, os
import subprocess

REQUIRED_PACKAGES = ["aiohttp", "customtkinter", "aiomysql"]


def install_missing_packages():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"Đang cài đặt {package}...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", package], check=True
            )


install_missing_packages()
# Tạo 1 trường nhập
root = tkinter.Tk()
root.withdraw()


class CreateConfig(customtkinter.CTkToplevel):

    def __init__(self, parent, filepath, title="Cài đặt Database"):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        self.filepath = filepath

        # Tạo window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        self.result: Optional[Dict[str, str]] = None
        self.grab_set()  # tạo modal

        self._create_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _create_widgets(self):
        # Frame chính
        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Lưu db?
        title_label = customtkinter.CTkLabel(
            main_frame, text="Lưu database", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 15))

        # thm frame nhỏ
        form_frame = customtkinter.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Host
        host_label = customtkinter.CTkLabel(form_frame, text="Máy chủ:")
        host_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.host_entry = customtkinter.CTkEntry(form_frame, width=220)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.host_entry.insert(0, "localhost")

        # Port
        port_label = customtkinter.CTkLabel(form_frame, text="Cổng:")
        port_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.port_entry = customtkinter.CTkEntry(form_frame, width=220)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        self.port_entry.insert(0, "3306")  # Mặc đinhj

        # User
        user_label = customtkinter.CTkLabel(form_frame, text="Người dùng:")
        user_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.user_entry = customtkinter.CTkEntry(form_frame, width=220)
        self.user_entry.grid(row=2, column=1, padx=5, pady=5)
        self.user_entry.insert(0, "root")

        # Password
        password_label = customtkinter.CTkLabel(form_frame, text="Mật khẩu:")
        password_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = customtkinter.CTkEntry(form_frame, width=220, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        # Nút
        button_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(15, 0))

        cancel_button = customtkinter.CTkButton(
            button_frame,
            text="Huỷ",
            command=self._on_cancel,
            fg_color="gray",
            hover_color="darkgray",
        )
        cancel_button.pack(side="left", padx=10)

        ok_button = customtkinter.CTkButton(
            button_frame, text="Lưu", command=self._on_ok
        )
        ok_button.pack(side="right", padx=10)

    def _on_ok(self):
        self.result = {
            "host": self.host_entry.get(),
            "port": self.port_entry.get(),
            "user": self.user_entry.get(),
            "password": self.password_entry.get(),
        }

        # Lưu file
        try:
            config = ConfigParser()
            if not config.has_section("database"):
                config.add_section("database")

            config.set("database", "host", self.result["host"])
            config.set("database", "port", self.result["port"])
            config.set("database", "user", self.result["user"])
            config.set("database", "password", self.result["password"])
            with open(self.filepath, "w") as configfile:
                config.write(configfile)
            messagebox.showinfo("Thành công", "Đã lưu thành công database")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu database,{e}")

        self.destroy()

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def get_input(self) -> Optional[Dict[str, str]]:
        self.wait_window()
        return self.result


class Database:
    def __init__(self, pool: Optional[aiomysql.Pool] = None) -> None:
        self.pool: aiomysql.Pool = pool  # gọi biến self.pool

    async def reconnect(
        self, db: str, file_path: str = None, **kwargs
    ):  # Thử nghiệm chưa chính thức
        if self.pool is not None:
            await self.close()
        if file_path:
            data = await self.load_config(file_path)
        else:
            # Lấy dữ liệu từ kwargs
            host = kwargs.get("host")
            port = kwargs.get("port", 3306)
            user = kwargs.get("user")
            password = kwargs.get("password")

            if not all([host, user, password]):
                raise ValueError("Thiếu thông tin host, user hoặc password để kết nối!")

            data = [host, port, user, password]

        await self.connect(*data, db=db)
        print("Đã kết nối trở lại database")

    @staticmethod
    async def check_internet_connection() -> str:  # kiểm tra kết nối internet
        try:
            with socket.create_connection(
                ("youtube.com", 80), timeout=5
            ):  # kiểm tra kết nối tới youtube cứ mỗi 5ms
                pass
        except:
            return "Không có kết nối internet hoặc kết nối yếu vui lòng thử lại nhé"
        return None

    @classmethod
    async def create_connect(
        cls,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
        minsize: int = 1,
        maxsize: int = 10,
        autocommit: bool = True,
    ):  # tạo kết nối db
        if host != "localhost":  # kiểm tra nếu không phải kết nôối local
            connection = (
                await cls.check_internet_connection()
            )  # lấy str từ kiểm tra check_internet_connection
            if connection:
                raise ConnectionError(connection)
            try:
                pool = await aiomysql.create_pool(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    db=db,
                    minsize=minsize,
                    maxsize=maxsize,
                    autocommit=autocommit,
                )  # tạo kết nối tới pool
                return cls(pool=pool)
            except Exception as e:
                raise e
            except aiomysql.Error as ae:
                raise ae

    async def connect(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        db: str,
        minsize: int = 1,
        maxsize: int = 10,
        autocommit: bool = True,
    ):  # hàm connect hoàn chỉnh
        self.pool = (
            await self.create_connect(
                host, port, user, password, db, minsize, maxsize, autocommit
            )
        ).pool
        return self

    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def execute(
        self, query: str, params: Tuple[Any] = None
    ) -> List[Tuple[Any]]:  # Thực hiện execute
        if not self.pool:
            raise Exception(
                "Kết nối database chưa được thiết lập,hãy kết nối với hàm connect/connected"
            )
        try:
            async with self.pool.acquire() as connection:
                con: aiomysql.Connection = connection
                async with con.cursor() as cursor:
                    cur: aiomysql.Cursor = cursor
                    await cur.execute(query, params)
                    if query.strip().upper().startswith("SELECT"):
                        return await cur.fetchall()
                    else:
                        await con.commit()
                        return cur.rowcount
        except Exception as e:
            raise e

    async def fetchall(
        self, query: str, params: Optional[Tuple] = None
    ) -> List:  # thực hiện fetch all
        if not self.pool:
            raise Exception(
                "Kết nối database chưa được thiết lập,hãy kết nối với hàm connect/connected"
            )
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

    async def fetchone(
        self, query: str, params: Optional[Tuple] = None
    ) -> List:  # thực hiện fetchone
        if not self.pool:
            raise Exception(
                "Kết nối database chưa được thiết lập,hãy kết nối với hàm connect/connected"
            )
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

    async def load_config(self, file_name: str) -> List[Tuple]:  # Load config
        if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
            config_data = CreateConfig(None, filepath=file_name).get_input()
            await self.load_config(file_name)
        config = ConfigParser()
        config.read(file_name)
        host = config.get("database", "host")
        port = config.getint("database", "port", fallback=3306)
        user = config.get("database", "user")
        password = config.get("database", "password")
        if not host or not user or not password:
            raise ValueError(
                "Missing one or more required database configuration fields: host, user, or password."
            )
        return [host, port, user, password]

    async def connected(self, db: str, file_name: str):
        data = await self.load_config(file_name=file_name)
        await self.connect(*data, db=db)

    async def help(self):
        """Hiển thị danh sách các phương thức có sẵn trong Database và cách sử dụng."""
        help_text = """
        📌 Database Helper 📌

        - **connected(db: str, file_name: str)**: Kết nối tới database với thông tin từ file config.
        - **connect(host, port, user, password, db, minsize=1, maxsize=10, autocommit=True)**: Kết nối database thủ công.
        - **close()**: Đóng kết nối database.
        - **execute(query: str, params: Tuple[Any] = None)**: Thực thi câu lệnh SQL (INSERT, UPDATE, DELETE, SELECT).
        - **fetchall(query: str, params: Optional[Tuple] = None)**: Lấy tất cả kết quả từ truy vấn.
        - **fetchone(query: str, params: Optional[Tuple] = None)**: Lấy một dòng dữ liệu từ truy vấn.
        - **executemany (query: str, params: List[Tuple])**: Thực thi nhiều câu lệnh SQL cùng lúc.
        ❗ Lưu ý: Trước khi sử dụng, hãy gọi `await database.connected("database_name", "config.cfg") nếu dùng connect`
        """
        print(help_text)

    async def executemany(self, query: str, params: List[Tuple]):
        if not self.pool:
            raise Exception(
                "Kết nối database chưa được thiết lập,hãy kết nối với hàm connect/connected"
            )
        try:
            async with self.pool.acquire() as connection:
                con: aiomysql.Connection = connection
                async with con.cursor() as cursor:
                    cur: aiomysql.Cursor = cursor
                    await cur.executemany(query, params)

                    await con.commit()
                    return cur.rowcount
        except Exception as e:
            raise e

    async def fetchmany(self, query: str, params: List[Tuple], size: int = 100):
        if not self.pool:
            raise Exception(
                "Kết nối database chưa được thiết lập,hãy kết nối với hàm connect/connected"
            )
        try:
            async with self.pool.acquire() as conn:
                connection: aiomysql.Connection = conn
                async with connection.cursor() as cursor:
                    cur: aiomysql.Cursor = cursor
                    await cur.execute(query, params)
                    results = await cur.fetchmany(size)
                    return results
        except Exception as e:
            raise e
