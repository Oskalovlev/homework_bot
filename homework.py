import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (APIRequestError, JSONError, ProblemKey,
                        StatusWorkError, WrongAPIResponseCodeError)

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    for item in ('PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID'):
        missing_tokens = []
        if not globals()[item]:
            missing_tokens.append(item)
        else:
            return True
        logging.critical(
            f'Нет обязательной/ых переменной/ых окружения: {missing_tokens}'
        )
        return False


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.error.TelegramError as error:
        logging.error(f'Ошибка отправки сообщения в телеграм {error}')
    else:
        logging.debug(f'Сообщение отправлено: {message}')


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
        if homework_statuses.status_code != HTTPStatus.OK:
            raise WrongAPIResponseCodeError(
                f'Ошибка ответа API. Статус: {homework_statuses.status_code}'
            )
        return homework_statuses.json()
    except requests.exceptions.JSONDecodeError as error:
        raise JSONError(f'Ошибка полученной информации из json: {error}')
    except requests.RequestException as error:
        raise APIRequestError(f'Ошибка запроса к API: {error}')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не словарь')
    if not response.get('homeworks'):
        raise KeyError('Ошибка словаря по ключу "homeworks"')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Ответ API по ключу "homeworks" не список')
    if not response.get('current_date'):
        raise ProblemKey('Ошибка по ключу "current_date"')
    if not isinstance(response['current_date'], int):
        raise ProblemKey('Ответ по ключу "current_date" не целое число')
    return response


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус."""
    if 'homework_name' not in homework:
        raise KeyError('Отсутствует ключ "homework_name"')
    if 'status' not in homework:
        raise KeyError('Отсутствует ключ "status"')
    homework_name = homework['homework_name']
    verdict = homework['status']
    if verdict not in HOMEWORK_VERDICTS:
        raise StatusWorkError(f'Неизвестный статус работы: {verdict}')
    verdict = HOMEWORK_VERDICTS[verdict]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    if not check_tokens():
        logging.critical('Как минимум, одна переменная окружения отсутствует')
        raise SystemExit(1)

    while True:
        try:
            response = get_api_answer(timestamp)
            homework = check_response(response)
            timestamp = response.get('current_date')
            homeworks = response.get('homeworks')
            if homeworks:
                homework = homeworks[0]
                message = parse_status(homework)
                send_message(bot, message)
        except ProblemKey:
            logging.error('Ошибка по ключу "current_date"')
        except Exception as error:
            logging.error(f'Что то сломалось при отправке, {error}')
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s [%(levelname)s] - '
            '%(name)s - %(message)s'
        ),
        handlers=[
            logging.FileHandler(f'{BASE_DIR}/output.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    main()
