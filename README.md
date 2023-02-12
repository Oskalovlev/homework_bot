# Homework bot.
Простой телеграмм-бот, который информирует меня (как студента) о статусе моей домашней работы.

### Обзор
Бот может взаимодействовать с API сайта Яндекс.Практикум и API мессенджера Telegram. Таким образом, если есть запрос к боту и есть ответ о статусе домашнего задания, бот отправит текстовое сообщение о результате в соответствующий чат.

### Технологии
```sh
Python 3.7.9
```
### Установка и запуск

ВАЖНАЯ ЗАМЕТКА!

This bot is designed to work specifically with my homework, so if you want to test the bot in practice, then you firtsly need to do the following:

create your own bot via @botfather and get a token
receive your own token via Yandex.Practicum website (you have to be the student)
put the data in the variables PRACTICUM_TOKEN, TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
Clone the repository and go to it using the command line:

```sh
git clone 
cd homework_bot
```
Create and activate a virtual environment:

## Windows:

```sh
py -3 -m venv env
. venv/Scripts/activate 
py -m pip install --upgrade pip
```
### macOS/Linux:

```sh
python3 -m venv .venv
source env/bin/activate
python3 -m pip install --upgrade pip
```

## Install dependencies from a file requirements.txt:

```sh
pip install -r requirements.txt
```

### Launch:

## Windows:

```sh
py homework.py 
```
## macOS/Linux:

```sh
python3 homework.py 
```
