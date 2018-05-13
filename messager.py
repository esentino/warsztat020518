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
    cnx = create_connection()
    cursor = cnx.cursor()
    user = User.get_user_by_email(cursor, email)
    if user:
        raise Exception("User Exists")
    else:
        user = User()
        user.email = email
        user.set_password(password)
        user.save_to_db()


def change_user_password(email, password, new_password):
    user = User.get_user_by_email()
    if user and check_password(password, user.hash_password) and len(new_password) > 8:
        user.set_password(new_password)
        user.save_to_db()


def delete_user(email, password):
    user = User.get_user_by_email(email)
    if user and check_password(password, user.hashed_password):
        user.delete()


def display_all_user():
    user_list = User.get_all_users()
    for user in user_list:
        print(" %s %s " % (user.username, user.email))

create_user("jan@pl.pl", "niepamietam")
