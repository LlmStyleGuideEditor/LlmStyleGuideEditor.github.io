from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from base64 import b64encode, b64decode
import sqlite3
import time
from User import User
from Translation import Translation


# Database connection
connection = sqlite3.connect('AutoSTEDB')
cursor = connection.cursor()


def register_user(username, password, commit=True):
    """Registers a user with the provided username and password
    :param username: the username to register with
    :param password: the plaintext password to register with
    :param commit: whether to immediately commit to database
    :return:
        None if a user of the given name exists
        User object if the user has been successfully registered
    """

    # Check if user exists
    cursor.execute("select * from users where username = ?", (username,))
    if len(cursor.fetchall()) != 0:
        return None

    # Generate salt
    salt_b64 = b64encode(get_random_bytes(32))

    # Get hashes
    password_hash_bytes, aes_key = scrypt(password, salt_b64.decode(), 32, 2**14, 8, 1, num_keys=2)
    password_hash_b64 = b64encode(password_hash_bytes)

    # Generate encryption/decryption key and encrypt with password
    key_bytes = get_random_bytes(32)
    cipher = AES.new(aes_key, AES.MODE_CCM)
    encrypted_key_bytes = cipher.encrypt(key_bytes)
    nonce = cipher.nonce
    encrypted_key_b64 = b64encode(encrypted_key_bytes)

    # Add everything to user database
    cursor.execute('insert into users (username, pw_salt, pw_hash, encrypted_key, key_nonce) values (?, ?, ?, ?, ?)',
                   (username, salt_b64, password_hash_b64, encrypted_key_b64, nonce))
    if commit:
        connection.commit()
    cursor.execute('select id from users where username = ?', (username,))
    user_id = cursor.fetchone()[0]

    # Return user object
    return User(user_id, username, aes_key)


def login_user(username, password):
    """Login a user with a username and password
    :param username: username (string)
    :param password: password (string)
    :return:
        User object if successfully logged in,
        None otherwise
    """

    # Get data from database
    cursor.execute("select * from users where username = ?", (username,))
    user_data = cursor.fetchone()

    # Check that user data exists
    if user_data is None:
        return None

    salt_b64 = user_data[2]

    password_hash, aes_key = scrypt(password, salt_b64, 32, 2**14, 8, 1, num_keys=2)

    test_hash = b64decode(user_data[3])

    # check for valid password
    if password_hash != test_hash:
        return None

    user_id = user_data[0]

    return User(user_id, username, aes_key)


def get_user_key(user):
    """Gets the user's data encryption key
    :param user: the user object
    :return: the user's data encryption key
    """
    cursor.execute("select * from users where username = ?", (user.username,))
    user_data = cursor.fetchone()

    encrypted_data_key = user_data[4]
    nonce = user_data[5]

    cipher = AES.new(user.key_encryption_key, AES.MODE_CCM, nonce=nonce)
    data_key = cipher.decrypt(encrypted_data_key)

    return data_key


def add_translation(user, in_text, out_text, commit=True):

    now = time.time()

    # TODO: encrypt
    cursor.execute("insert into translation_log (user_id, timestamp, input, output) values (?, ?, ?, ?)",
                   (user.user_id, now, in_text, out_text))
    if commit:
        connection.commit()

    return Translation(user.user_id, now, in_text, out_text)


def get_translations(user):

    # TODO: decrypt
    cursor.execute("select * from translation_log where user_id = ?", (user.user_id,))

    return [Translation(data_row[1], data_row[2], data_row[3], data_row[4]) for data_row in cursor.fetchall()]


if __name__ == '__main__':
    print(repr(user := login_user("uid", "upass")))
    print(repr(add_translation(user, "Hello World 2", "Hello World 2")))
    print(repr(get_translations(user)))
