class NotForSendingError(Exception):
    pass


class TelegramError(NotForSendingError):
    """Высылает, когда выслать в телеграм. НЕ шлём в телеграм"""
    pass


class EmptyAPIResponseError(NotForSendingError):
    """Вылетает, когда нет домашней работы или timestamp. НЕ шлём в телеграм"""
    pass


class WrongAPIResponseCpdeError(Exception):
    """Вылетает, когда ответ сервера !=200. ШЛЁМ в телеграм"""
    pass


class ConnectionError(Exception):
    """Вылетает, когда произошла ошибка подключения к серверу"""
    pass