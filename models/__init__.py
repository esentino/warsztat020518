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
    __id = None
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

    def save_to_db(self):
        pass

    def set_password(self, new_password):
        self.__hashed_password=new_password

    @property
    def hashed_password(self):
        return self.__hashed_password

    def delete(self):
        pass

    @staticmethod
    def get_all_users():
        return [User(), User()]
