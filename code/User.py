class User:
    def __init__(self, user_id, username, encrypt_bytes):
        self.user_id = user_id
        self.username = username
        self.encrypt_key = encrypt_bytes

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'{self.user_id=} {self.username=} {self.encrypt_key=}'
