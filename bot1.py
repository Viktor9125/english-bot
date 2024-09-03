import json
import random
import telebot

TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)

questions = ['как тебя зовут', 'hello', 'привет', 'как дела']
answers = ['Меня зовут bot1.', 'Hello!', 'Привет!', 'Отлично.']

try:
    with open('user_data.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет!')
    bot.send_message(message.chat.id, 'Я bot1.')
    bot.send_message(message.chat.id, '/help - помощь.')


@bot.message_handler(commands=["learn"])
def handle_learn(message):
    # chat_id = message.chat.id
    # if len(message.text) > 6:
    #     user_words = user_data.get(str(chat_id), {})
    #     words_number = int(message.text.split()[1])
    #     send_words = []
    #     random_key = random.choice(list(user_words.keys()))
    #     if len(user_words) >= words_number:
    #         for message in range(words_number):
    #             while random_key in send_words:
    #                 random_key = random.choice(list(user_words.keys()))
    #             bot.send_message(chat_id, random_key)
    #             send_words.append(random_key)
    #     else:
    #         bot.send_message(chat_id, 'Ошибка 1.')
    #         bot.send_message(chat_id, '/help - помощь.')
    # else:
    #     bot.send_message(chat_id, 'Ошибка 2.')
    #     bot.send_message(chat_id, '/help - помощь.')

    try:
        if len(message.text) > 6:
            user_words = user_data.get(str(message.chat.id), {})

            words_number = int(message.text.split()[1])

            ask_translation(message.chat.id, user_words, words_number)
        else:
            bot.send_message(message.chat.id, 'Ошибка 2.')
            bot.send_message(message.chat.id, '/help - помощь.')
    except ValueError:
        bot.send_message(message.chat.id, 'Произошла ошибка ValueError.')
    except IndexError:
        bot.send_message(message.chat.id, 'Произошла ошибка IndexError.')


def ask_translation(chat_id, user_words, words_left):
    if 0 < words_left <= len(user_data[str(chat_id)]):
        word = random.choice(list(user_words.keys()))
        translation = user_words[word]
        bot.send_message(chat_id, f'Напиши перевод слова {word}.')

        words_left -= 1
        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        if words_left > len(user_data[str(chat_id)]):
            bot.send_message(chat_id, 'Ошибка 1.')
            bot.send_message(chat_id, '/help - помощь.')
        else:
            bot.send_message(chat_id, 'Урок закончен.')


def check_translation(message, translation, words_left):
    user_translation = message.text.strip().lower()

    if user_translation == translation.lower():
        bot.send_message(message.chat.id, 'Правильно!')
    else:
        bot.send_message(message.chat.id, f'Неправильно. Правильный перевод {translation}.')

    ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left)


@bot.message_handler(commands=["add_word"])
def handle_add_word(message):
    try:
        global user_data
        chat_id = message.chat.id
        user_dict = user_data.get(str(chat_id), {})
        words = message.text.split()[1:]

        if len(words) == 2:
            word, translation = words[0].lower(), words[1].lower()
            user_dict[word] = translation

            user_data[str(chat_id)] = user_dict

            # user_data[chat_id][word] = [translation]
            # print(user_data)

            with open('user_data.json', 'w', encoding='utf-8') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=4)

            bot.send_message(chat_id, f'Слово {word} добавлено в словарь.')
            bot.send_message(chat_id, f'Текущая длина словаря {len(user_data[str(chat_id)])}.')
        else:
            bot.send_message(chat_id, 'Ошибка 2.')
            bot.send_message(chat_id, '/help - помощь.')
    except Exception as e:
        bot.send_message(chat_id, f'Произошла ошибка {e}.')


@bot.message_handler(commands=["help"])
def handle_help(message):
    bot.send_message(message.chat.id, 'Я бот для изучения английского языка.')
    bot.send_message(message.chat.id, 'У меня есть команды')
    bot.send_message(message.chat.id, '/help')
    bot.send_message(message.chat.id, '/learn количество слов')
    bot.send_message(message.chat.id, '/add_word 1 слово 2 слово')
    bot.send_message(message.chat.id, 'Ошибки')
    bot.send_message(message.chat.id, '1 - число больше чем слов в словаре.')
    bot.send_message(message.chat.id, '2 - неправильно вызвана команда.')
    bot.send_message(message.chat.id, 'Мой автор Виктор.')


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    # if message.text.lower() == 'как тебя зовут':
    #     bot.send_message(message.chat.id, 'Меня зовут bot1.')
    # elif message.text.lower() == 'hello':
    #     bot.send_message(message.chat.id, 'Hello!')
    # elif message.text.lower() == 'привет':
    #     bot.send_message(message.chat.id, 'Привет!')
    # elif message.text.lower() == 'как дела':
    #     bot.send_message(message.chat.id, 'Отлично.')
    # else:
    #     bot.send_message(message.chat.id, 'Ответ не найден...')
    if message.text.lower() in questions:
        answer_index = questions.index(message.text.lower())
        bot.send_message(message.chat.id, answers[answer_index])
    else:
        bot.send_message(message.chat.id, 'Ответ не найден...')


if __name__ == '__main__':
    bot.polling(none_stop=True)
