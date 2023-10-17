import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6671504237:AAFjo5EzGooZj9BJ6zPf06-Ag6eMI3ASdYA",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Намяукать о себе"  # Можно менять текст
text_button_1 = "Я котик веселотик"  # Можно менять текст
text_button_2 = "Я котик грустнотик"  # Можно менять текст
text_button_3 = "Я котик усталотик"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Мяу! Пусть эти котики сделают твой день мурмяушным) ',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Ваше _мяу-имя?_')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Приятно помяукаться! *Ваш* мяу-возраст?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id,
                     'Муррчу от такого замечательного знакомства! Выбирай скорее, какой ты котик сегодня',
                     reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[котик веселотик](https://damion.club/uploads/posts/2022-11/1669023352_damion-club-p-kot-ulibaka-vkontakte-74.jpg)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[котик грустнотик](https://haski-mana.ru/wp-content/uploads/3/0/6/3065f9fc6a9928a61e6894a4e6634afb.jpeg)",
                     reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id,
                     "[котик усталотик](https://i.pinimg.com/originals/df/fc/29/dffc295da7d4226dab07a7891d05faab.jpg)",
                     reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()