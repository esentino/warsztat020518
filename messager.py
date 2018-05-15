"""Messanger."""
from clcrypto import check_password
from models import User
from psycopg2 import connect, OperationalError


def create_connection(db_name="exercises_db"):
    """
    Tworzenie połączenia do bazy danych
    :param db_name:
    :return:
    """
    username = "postgres"
    password = "coderslab"
    host = "localhost"

    try:
        connection = connect(user=username, password=password, host=host, dbname=db_name)
        return connection
    except OperationalError:
        return None


def create_user(email, password):
    """
    Pierwszy scenariusz tworzenie użyszkodnika
    :param email: email
    :param password: hasło
    :return:
    """
    try:
        cnx = create_connection()
        cursor = cnx.cursor()
        user = User.get_user_by_email(cursor, email)
        if user:
            cursor.close()
            cnx.close()
            raise Exception("User Exists")
        else:
            user = User()
            user.email = email
            user.set_password(password)
            user.save_to_db(cursor)
            cnx.commit()
            cursor.close()
            cnx.close()
    except OperationalError:
        print("Problem z połączeniem do bazy danych")

def change_user_password(email, password, new_password):
    """
    Zmiana hasła użytkownika
    :param email: email
    :param password: stare hasło
    :param new_password: nowe hasło
    :return:
    """
    try:
        cnx = create_connection()
        cursor = cnx.cursor()
        user = User.get_user_by_email(cursor, email)
        if user and check_password(password, user.hashed_password) and len(new_password) > 8:
            user.set_password(new_password)
            user.save_to_db(cursor)
            cnx.commit()
        cursor.close()
        cnx.close()
    except OperationalError:
        print("Problem z połączeniem do bazy danych")

def delete_user(email, password):
    """
    Usunięcie użytkownika
    :param email: email
    :param password: hasło
    :return: None
    """
    try:
        cnx = create_connection()
        cursor = cnx.cursor()
        user = User.get_user_by_email(cursor, email)
        if user and check_password(password, user.hashed_password):
            user.delete(cursor)
            cnx.commit()
        cursor.close()
        cnx.close()
    except OperationalError:
        print("Problem z połączeniem do bazy danych")


def display_all_user():
    """
    Wyświetlanie wszystkich użytkowników.
    :return: None
    """
    try:
        cnx = create_connection()
        cursor = cnx.cursor()
        user_list = User.get_all_users(cursor)
        for user in user_list:
            print(" %s %s " % (user.username, user.email))
        cursor.close()
        cnx.close()
    except OperationalError:
        print("Problem z połączeniem do bazy danych")


USER_MAIL = "jan@pl.pl"
USER_PASSWORD = "niepamietam"
USER_NEW_PASSWORD = "juzpamietam"
create_user(USER_MAIL, USER_PASSWORD)
display_all_user()
change_user_password(USER_MAIL, USER_MAIL, USER_NEW_PASSWORD)
delete_user(USER_MAIL, USER_NEW_PASSWORD)
display_all_user()
