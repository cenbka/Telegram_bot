from random import randint
import telebot
import time


bot = telebot.TeleBot('****')
count = 0   # Счетчик кол-ва попыток
n = 0       # Счетчик неправильного ввода
# games = 0
last_time = {}


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_messages(message):     # Инструкция для работы бота
    if message.text == 'Привет' or message.text == '/start':
        bot.send_message(message.from_user.id, "Привет, игра угадай число, введи число от 0 до 1000!")
        # bot.register_next_step_handler(message, start);
        users = {}
        value = 'Ваше значение'
        users.update({message.chat.id: value})
        rand(message)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def rand(message):      # Создается число, которое нужно отгадать
    global number
    number = randint(1, 1000)
    print(number)
    bot.register_next_step_handler(message, start)
    return number


def start(message):     # Вводим числа
    num = message.text
    if not num.isdigit() or num == 0:
        is_valid(message)
    if num.isdigit():
        num = int(num)
        if num > 1000:
            is_valid(message)

        elif num < 0:
            is_valid(message)

        elif 0 <= num < 1001:
            correct(message)


def correct(message):               # Угадываем число
    global count
    n = message.text
    n = int(n)
    if n == number:
        count += 1
        bot.send_message(message.from_user.id, 'Поздравляем! Ты угадал число, игра окончена.')
        bot.send_message(message.from_user.id, f'Кол-во твоих попыток: {count}')
        print(f'Угадал с {count}')
        new_game(message)
    elif n > number:
        count += 1
        bot.send_message(message.from_user.id, f'Меньше числа {n}')
        bot.register_next_step_handler(message, start)
        print(f'Попытки: {count}')
    else:
        count += 1
        bot.send_message(message.from_user.id, f'Больше числа {n}')
        bot.register_next_step_handler(message, start)
        print(f'Попытки: {count}')


def is_valid(message):  # Проверка корректности числа
    global n
    global count
    count += 1
    v = bot.reply_to(message, 'Напиши число от 0 до 1000')
    bot.register_next_step_handler(v, start)
    n += 1
    print(f'Кол-во неправильного ввода {n}')


def new_game(message):
    global count
    global n
    count = 0
    n = 0
    time.sleep(5)
    bot.send_message(message.from_user.id, "Новая игра, введи число от 0 до 1000!")
    rand(message)


bot.polling(none_stop=True, interval=0)