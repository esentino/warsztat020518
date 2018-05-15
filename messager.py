from clcrypto import check_password
from models import User, Message
from psycopg2 import connect, OperationalError


def create_connection(db_name = "exercises_db"):
    username = "postgres"
    password = "coderslab"
    host= "localhost"

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

def change_user_password(email, password, new_password):
    """
    Zmiana hasła użytkownika
    :param email: email
    :param password: stare hasło
    :param new_password: nowe hasło
    :return:
    """
    user = User.get_user_by_email()
    if user and check_password(password, user.hash_password) and len(new_password) > 8:
        user.set_password(new_password)
        user.save_to_db()


def delete_user(email, password):
    """
    Usunięcie użytkownika
    :param email: email
    :param password: hasło
    :return: None
    """
    user = User.get_user_by_email(email)
    if user and check_password(password, user.hashed_password):
        user.delete()


def display_all_user():
    """
    Wyświetlanie wszystkich użytkowników.
    :return: None
    """
    user_list = User.get_all_users()
    for user in user_list:
        print(" %s %s " % (user.username, user.email))


user_email = "jan@pl.pl"
user_password = "niepamietam"
user_new_password = "juzpamietam"
create_user(user_email, user_password)
display_all_user()
change_user_password(user_email, user_email, user_new_password)
delete_user(user_email, user_new_password)
display_all_user()
