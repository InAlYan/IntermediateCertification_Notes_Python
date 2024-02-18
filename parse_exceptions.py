class ParseIntException(Exception):
    def __init__(self, message, val):
        self.val_to_int = val
        self.message = message

    def __str__(self):
        return f"ParseIntException: {self.message} {self.val_to_int}"


class ParseDateTimeException(Exception):
    def __init__(self, message, val):
        self.val_to_int = val
        self.message = message

    def __str__(self):
        return f"ParseDateTimeException: {self.message} {self.val_to_int}"
