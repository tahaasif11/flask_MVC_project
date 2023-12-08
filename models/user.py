from utilities.helper import cursor, connection


def insert_into_users(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birthday = data.get('birthday')
    age = data.get('age')
    description = data.get('description')

    user_data = (name, email, password, birthday,age,description)
    cursor.execute("""
            INSERT INTO users
            (name,email, password,birthday,age,description)
            VALUES (%s,%s,%s,%s,%s)""", user_data)
    connection.commit()


def login(data):
    email = data.get('email')
    password = data.get('password')
    cursor.execute("""SELECT * FROM users WHERE email=%s AND password=%s""", (email, password))
    return cursor.fetchone()


def find_user_by_email(email):
    cursor.execute("""SELECT * FROM users WHERE email=%s """, email)
    return cursor.fetchone()


def update_user_password(email, password):
    cursor.execute(""" UPDATE users SET password=%s WHERE email=%s """, (password, email))
    connection.commit()


def all_users():
    cursor.execute("""SELECT * FROM users """)
    return cursor.fetchall()


def find_user_by_id(id):
    cursor.execute("""SELECT * FROM users WHERE id=%s """, id)
    return cursor.fetchone()


def update_user(data, id):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    birthday = data.get('birthday')
    age = data.get('age')
    description = data.get('description')
    user_data = (name, email, password, birthday, age, description, id)

    cursor.execute("""
        UPDATE users SET name=%s, email=%s, password=%s, birthday=%s, age=%s, description=%s WHERE id=%s """, user_data)
    connection.commit()