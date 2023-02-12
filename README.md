# Homework bot
Простой телеграмм-бот, который информирует меня (как студента) о статусе моей домашней работы.

### Обзор
Бот может взаимодействовать с API сайта Яндекс.Практикум и API мессенджера Telegram. Таким образом, если есть запрос к боту и есть ответ о статусе домашнего задания, бот отправит текстовое сообщение о результате в соответствующий чат.

## Технологии

```sh
Python 3.7.9
```

## Установка и запуск

### ВАЖНАЯ ЗАМЕТКА!
Этот бот предназначен для работы именно с моими домашними заданиями, поэтому если вы хотите протестировать бота на практике, то вам в первую очередь нужно сделать следующее:
#### - создай своего бота через @botfather и получи токен
#### - получить собственный токен через сайт [Яндекс.Практикум](https://practicum.yandex.ru/) (вы должны быть студентом)
#### - поместите данные в переменные PRACTICUM_TOKEN, TELEGRAM_TOKEN и TELEGRAM_CHAT_ID

## Клонируем репозиторий и переходим к нему с помощью командной строки:

```sh
git clone 
cd homework_bot
```

## Создайте и активируйте виртуальную среду:

### Windows:
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

## Установите зависимости из файла requirements.txt:

```sh
pip install -r requirements.txt
```

## Запуск:

### Windows:
```sh
py homework.py 
```

### macOS/Linux:
```sh
python3 homework.py 
```

## License
### MIT
