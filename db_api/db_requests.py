import sqlite3

class Database:
    def __init__(self, db_path='shop_database.db'):
        self.db_path = db_path

    @property
    def connection(self):
        return sqlite3.connect(self.db_path)

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):  # fetchone - если мы делаем запрос и должна вернутся одна запись ,
                                                                # fetchall - если нужно из запроса несколько (все)
                                                                # commit - если вносим в БД изменения
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users(
        id int NOT NULL,
        phone text,
        PRIMARY KEY (id)
        );
        """

        self.execute(sql, commit=True)

    def add_user(self, id: int, phone: str = None):
        sql = 'INSERT INTO Users(id, phone) VALUES(?,?)'
        parameters = (id, phone)
        self.execute(sql, parameters, commit=True)

    def select_user_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Users WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_all_users(self) -> list:
        sql = "SELECT * FROM Users "
        return self.execute(sql, fetchall=True)

    def update_user_phone(self, id: int, phone: str):
        sql = "UPDATE Users SET phone=? WHERE id=?"
        return self.execute(sql, parameters=(phone, id), commit=True)

    def delete_user(self, **kwargs):
        sql = "DELETE FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return self.execute(sql, parameters=parameters, commit=True)




## ЗДЕСЬ СДЕЛАТЬ ТОВАРЫ
    def create_table_products(self):
        sql = """
        CREATE TABLE Products(
        id int NOT NULL,
        title text,
        count int,
        photo_path text,
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_product(self, id: int, title: str = None, count: int = 0, photo_path: str = ''):
        sql = 'INSERT INTO Products(id, title, count, photo_path) VALUES(?, ?, ?, ?)'
        parameters = (id, title, count, photo_path)
        self.execute(sql, parameters, commit=True)

    def select_product_info(self, **kwargs) -> list:
        sql = 'SELECT * FROM Products WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def select_all_products(self) -> list:
        sql = "SELECT * FROM Products "
        return self.execute(sql, fetchall=True)

    def get_product_count(self) -> int:
        sql = "SELECT * FROM Products"
        return len(self.execute(sql, fetchall=True))

    def update_product_count(self, count: int, title: str):
        sql = "UPDATE Products SET title=? WHERE count=?"
        return self.execute(sql, parameters=(title, count), commit=True)

    @staticmethod
    def format_args(sql, parameters: dict) -> tuple:
        sql += " AND ".join([
            f"{product} = ?" for product in parameters
        ])
        return sql, tuple(parameters.values())

## Корзина
    def create_table_basket(self):
        sql = """
        CREATE TABLE Basket(
        id int NOT NULL,
        user_basket text,
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_product_basket(self, id: int, user_basket: str = None):
        sql = 'INSERT INTO Basket(id, user_basket) VALUES(?,?)'
        parameters = (id, user_basket)
        self.execute(sql, parameters, commit=True)

    def select_user_basket(self, **kwargs) -> tuple[int, str]:
        sql = 'SELECT * FROM Basket WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        data = self.execute(sql, parameters, fetchone=True)
        if data is None:
            self.add_product_basket(id=kwargs['id'])
            data = (kwargs['id'], '')
        return data

    def update_basket(self, id: int, user_basket: str):
        sql = "UPDATE Basket SET user_basket=? WHERE id=?"
        return self.execute(sql, parameters=(user_basket, id), commit=True)

    def select_all_basket(self) -> list:
        sql = "SELECT * FROM Basket "
        return self.execute(sql, fetchall=True)

    def delete_all(self):
        self.execute("DELETE FROM Users WHERE True", commit=True)
        self.execute("DELETE FROM Products WHERE True", commit=True)
        self.execute("DELETE FROM Basket WHERE True", commit=True)

    def drop_all(self):
        self.execute("DROP TABLE Users", commit=True)
        self.execute("DROP TABLE Products", commit=True)
        self.execute("DROP TABLE Basket", commit=True)




## Купить