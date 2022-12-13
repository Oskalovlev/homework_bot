class NotForSendingError(Exception):
    """Нет докстринга."""

    pass


class TelegramError(NotForSendingError):
    """
    Вылетает, когда не получилось отправить в телеграм.
    НЕ шлём в телеграм.
    """

    pass


class EmptyAPIResponseError(NotForSendingError):
    """
    Вылетает, когда нет домашней работы или timestamp.
    НЕ шлём в телеграм.
    """

    pass


class WrongAPIResponseCodeError(Exception):
    """Вылетает, когда ответ сервера !=200. ШЛЁМ в телеграм."""

    pass


class ConnectionError(Exception):
    """Вылетает, когда произошла ошибка подключения к серверу."""

    pass
