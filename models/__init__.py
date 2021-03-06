from clcrypto import password_hash
from .message import Message


"""
CREATE TABLE Users(
id serial,
username varchar(255),
email varchar(255) UNIQUE,
hashed_password varchar(255),
PRIMARY KEY (id)
);
"""


class User:
    __id = -1
    username = None
    __hashed_password = None
    email = None

    @staticmethod
    def get_user_by_email(cursor, email):
        """
        Zwraca użytkownika po jego adresie email
        :param cursor:
        :param email:
        :return:
        """
        sql = "SELECT id, username, email, hashed_password FROM users WHERE email=%s"
        cursor.execute(sql, (email,))  # (email, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user

    def save_to_db(self, cursor):
        """
        Zapisuje/Aktualizuje użytkownika do bazy danych
        :param cursor:
        :return:
        """
        if self.__id == -1:
            sql = """
                INSERT INTO Users(username, email, hashed_password)
                VALUES (%s, %s, %s) RETURNING id;
            """
            cursor.execute(sql, (self.username, self.email, self.hashed_password))
            (id,) = cursor.fetchone()
            self.__id = id
            return True

        sql = """
            UPDATE Users 
            SET username = %s, email = %s, hashed_password = %s
            WHERE id = %s"""
        cursor.execute(sql, (self.username, self.email, self.hashed_password, self.__id))
        return True

    def set_password(self, new_password):
        """
        Ustawia nowe hasło użytkownikowi
        :param new_password:
        :return:
        """
        self.__hashed_password=password_hash(new_password)

    @property
    def hashed_password(self):
        """zwraca zahashowane hasło"""
        return self.__hashed_password

    def delete(self, cursor):
        """
        Usuwa użytkownika oraz ustawia jego id na -1
        :param cursor:
        :return:
        """
        sql = """DELETE FROM users WHERE email = %s"""
        cursor.execute(sql, (self.email,))  # (email, ) - bo tworzymy krotkę
        self.__id = -1

    @staticmethod
    def get_all_users(cursor):
        """
        Zwraca listę użytkowników
        :param cursor:
        :return:
        """
        sql = """ SELECT id, username, email, hashed_password FROM users """
        cursor.execute(sql)
        user_list = []
        for user_row in cursor:
            user = User()
            user.__id = user_row[0]
            user.username = user_row[1]
            user.email = user_row[2]
            user.__hashed_password = user_row[3]
            user_list.append(user)
        return user_list
