class Translation:

    def __init__(self, user_id, timestamp, in_text, out_text):
        self.user_id = user_id
        self.timestamp = timestamp
        self.in_text = in_text
        self.out_text = out_text

    def __str__(self):
        return self.out_text

    def __repr__(self):
        return f'{self.user_id=} {self.timestamp=} {self.in_text=} {self.out_text=}'
