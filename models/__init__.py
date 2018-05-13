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
        if self.__id == -1:
            sql = """
                INSERT INTO Users(username, email, hashed_password)
                VALUES (%s, %s, %s) RETURNING id;
            """
            cursor.execute(sql, (self.username, self.email, self.hashed_password))
            (id,) = cursor.fetchone()
            self.__id = id
            return True

    def set_password(self, new_password):
        self.__hashed_password=password_hash(new_password)

    @property
    def hashed_password(self):
        return self.__hashed_password

    def delete(self):
        raise NotImplementedError

    @staticmethod
    def get_all_users():
        return [User(), User()]
