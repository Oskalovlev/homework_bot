class NotForSendingError(Exception):
    """Нет докстринга."""

    pass


class APIRequestError(NotForSendingError):
    """
    Вылетает, когда нет домашней работы или timestamp.
    НЕ шлём в телеграм.
    """

    pass


class WrongAPIResponseCodeError(Exception):
    """Вылетает, когда ответ сервера !=200. ШЛЁМ в телеграм."""

    pass


class StatusWorkError(APIRequestError):
    """Статус работы не известен."""

    pass


class JSONError(Exception):
    """Ошибка в json."""

    pass


class ProblemKey(TypeError):
    """Ошибка ключа."""

    pass
