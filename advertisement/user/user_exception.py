class NotUserException(Exception):

    def __init__(self, user_name):
        super().__init__()
        self.user_name = user_name

    def __str__(self):
        return f'{self.user_name} does not exist'


class NotUserCodeException(Exception):

    def __str__(self):
        return f'Code does not exist'


class TimeOutCodeException(Exception):

    def __str__(self):
        return f'Code timeout'


class CodeDoNotMatchException(Exception):

    def __str__(self):
        return f'Code do not match'


class EmailAlreadyRegistered(Exception):

    def __str__(self):
        return f'This email is already registered'


