import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

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
    if all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]):
        return True

    environment_variables = [
        ('PRACTICUM_TOKEN', PRACTICUM_TOKEN),
        ('TELEGRAM_TOKEN', TELEGRAM_TOKEN),
        ('TELEGRAM_CHAT_ID', TELEGRAM_CHAT_ID),
    ]
    for name, env in environment_variables:
        if not env:
            logging.critical(f'Отсутствует переменная окружения: '
                             f'{name} Программа принудительно остановлена.')
    return False


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f'Сообщение в чат {TELEGRAM_CHAT_ID}: {message}')
        raise logging.debug(f'Получен новый статус домашней работы: {message}')
    except Exception:
        logging.error('Ошибка отправки сообщения в телеграм')


def get_api_answer(timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(
            ENDPOINT,
            headers=HEADERS,
            params=params
        )
    except Exception as error:
        raise Exception(f'Ошибка запроса к API: {error}')
    if homework_statuses.status_code != HTTPStatus.OK:
        status_code = homework_statuses.status_code
        raise Exception(f'Ошибка {status_code}')
    try:
        return homework_statuses.json()
    except ValueError:
        raise ValueError('Ошибка полученной информации из json')


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Ответ API не словарь')
    if not response.get('homeworks'):
        raise KeyError('Ошибка словаря по ключу "homeworks"')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Ответ API по ключу "homeworks" не список')
    if response.get('homeworks'):
        return response


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе статус."""
    if 'homework_name' not in homework:
        raise KeyError('Отсутствует ключ "homework_name"')
    if 'status' not in homework:
        raise Exception('Отсутствует ключ "status"')
    homework_name = homework['homework_name']
    verdict = homework['status']
    if verdict not in HOMEWORK_VERDICTS:
        raise Exception(f'Неизвестный статус работы: {verdict}')
    verdict = HOMEWORK_VERDICTS[verdict]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    if not check_tokens():
        logging.critical('Как минимум, одна переменная окружения отсутствует')
        sys.exit()

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
            time.sleep(RETRY_PERIOD)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
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
