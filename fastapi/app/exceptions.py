class MovieNotFoundException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IncorrectCategory(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
