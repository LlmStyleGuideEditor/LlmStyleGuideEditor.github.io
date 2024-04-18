from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from base64 import b64encode, b64decode
import sqlite3
from User import User


# Database connection
connection = sqlite3.connect('users')
cursor = connection.cursor()


def register_user(username, password):
    """Registers a user with the provided username and password
    :param username: the username to register with
    :param password: the plaintext password to register with
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
    cursor.execute('select id from users where username = ?', (username,))
    user_id = cursor.fetchone()[0]

    # Return user object
    return User(user_id, username, key_bytes)


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

    # otherwise get user id and data key
    user_id = user_data[0]

    encrypted_key = b64decode(user_data[4])
    nonce = user_data[5]
    cipher = AES.new(aes_key, AES.MODE_CCM, nonce)
    data_key = cipher.decrypt(encrypted_key)

    return User(user_id, username, data_key)


if __name__ == '__main__':
    print(repr(register_user('Emoji', ' ')))
    print(repr(login_user('Emoji', ' ')))
