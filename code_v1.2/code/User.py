class User:
    def __init__(self, user_id, username, key_encryption_key):
        self.user_id = user_id
        self.username = username
        self.key_encryption_key = key_encryption_key

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'{self.user_id=} {self.username=} {self.key_encryption_key=}'
