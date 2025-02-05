import psycopg2

import os


class DataBase:
    _instance = None
    _ip_address = os.getenv('IP_ADDRESS')
    _db_name = os.getenv('DB_NAME')
    _user_name = os.getenv('DB_USER_NAME')
    _password = os.getenv('DB_PASSWORD')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = psycopg2.connect(
            user=self._user_name,
            password=self._password,
            dbname=self._db_name,
            host=self._ip_address,
            port=5431,
        )
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

    # @staticmethod
    # def extract_kwargs(sql: str, parameters: dict, _and: bool = True) -> tuple:
    #     sql += (' AND ' if _and else ', ').join([f'{key} = ?' for key in parameters])
    #     return sql, tuple(parameters.values())

    def create_main_table(self):
        sql = f'''CREATE TABLE IF NOT EXISTS wishlist_table(
            wish_id             SERIAL PRIMARY KEY,
            user_id             SERIAL,
            description         CHARACTER VARYING(500),
            picture_id          CHARACTER VARYING(500),
            link                CHARACTER VARYING(500)
            )'''
        self.execute(sql, commit=True)

    def add_wish(self,
                 user_tg_id: int,
                 description: str,
                 pict_id: str = None,
                 link: str = None):
        sql = f'INSERT INTO wishlist_table (user_id, description, picture_id, link) VALUES (%s, %s, %s, %s)'
        self.execute(sql, (user_tg_id, description, pict_id, link), commit=True)

    def get_wishes(self, user_tg_id: int):
        sql = 'SELECT * FROM wishlist_table WHERE user_id=%s'
        return self.execute(sql, (user_tg_id,), fetchall=True)
