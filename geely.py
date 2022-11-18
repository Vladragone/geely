from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.utils.markdown import hlink
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import json
from asyncio import sleep

token = "5717297177:AAG8CZkVFz-yfhEy1odm1mx4KafbDAUwasw"

bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class change(StatesGroup):
    start_pos = State()
    ss = State()
    adding_number = State()
    check_number = State()
    check_house = State()
    write_house = State()
    add_photo = State()
@dp.message_handler(commands=["start"])
async def start_message(message):
    user = message.from_user.username
    if str(message.chat.id) == "-840472225":
        with open("base.json","r",encoding="utf-8") as file:
            file = file.read()

        file = json.loads(file)
        
        s = ''
        n = 30
        for i in range(len(list(file.items()))):
                    
            s += str(list(file.items())[i]) + "\n"
                    
            if i == n:
                n += 30
                await bot.send_message(message.chat.id,s)
                await sleep(3)
                s = ""
        await bot.send_message(message.chat.id,f"Всего в базе человек - {len(list(file.keys()))}")
            
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    try:
        check = file[str(message.chat.id)][2]
    except:
        check = 0
    if check == "Неизвестный пользователь" and user != None:
        file[str(message.chat.id)] = [0,0,str(message.from_user.username),False]
    elif check == 0:
        if message.from_user.username == None:
            file[str(message.chat.id)] = [0,0,"Неизвестный пользователь",False]
        else:
            file[str(message.chat.id)] = [0,0,str(message.from_user.username),False]
    kb = [[types.KeyboardButton(text="Добавить свой номер"),types.KeyboardButton(text="Проверить номер")],[types.KeyboardButton(text="Найти владельцев по области")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True,one_time_keyboard=True)
    with open("base.json", "w",encoding="utf-8") as my_file:
        my_file.write(json.dumps(file))
    photo = open(f"image/start_photo.png","rb")
    await bot.send_photo(message.chat.id,photo,"Привет, друг! Здесь ты можешь найти своих соседей по району или какой-то конкретный автомобиль.\nПеред тем как добавлять авто убедитесь что у вас есть НИК в телеграм - как это? Смотрите фото сверху!\nТакже ты можешь добавить свой номер, чтобы другие могли найти тебя :)\nПеред добавлением своего авто - проверь наличие ник-нейма в телеграм\nДля продолжения выбери одну из кнопок снизу. Если бот не работает - /start в помощь :)",reply_markup=keyboard)
    await change.ss.set()
@dp.message_handler(state=change.ss)
async def check(message, state:FSMContext):
    if message.text == "Добавить свой номер":
        await bot.send_message(message.chat.id, "Отправьте номер вашего авто формата А000АА000. ВНИМАНИЕ! Использовать строго РУССКИЕ ЗАГЛАВНЫЕ буквы (например E633CC799)")
        await change.adding_number.set()
    elif message.text == "Проверить номер":
        await bot.send_message(message.chat.id, "Введите номер авто на РУССКОЙ раскладке ЗАГЛАВНЫМИ буквами для проверки участника (например E633CC799)")
        await change.check_number.set()
    elif message.text == "Найти владельцев по области":
        await bot.send_message(message.chat.id, "А теперь необходимо узнать твой город или район Москвы. Пример: «Одинцово, Сергиев Посад, Южное Бутово, Комсомольский район, Ростов-на-Дону» и т.д.\nРайоны Москвы указывать так ( Выхино, Ломоносовский район, Бибирево)\nТОЛЬКО 1 ГОРОД или РАЙОН!\nНЕ НАДО ПИСАТЬ - МОСКВА ВЫХИНО и МОСКВА ЛОМОНОСОВСКИЙ")
        await change.check_house.set()
    else:
        await start_message(message)
@dp.message_handler(state=change.check_house)
async def find_region(message,state:FSMContext):
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    flag = True
    for i in file.keys():

        if file[i][1] == message.text:
            try:
                photo = open(f"image/{i}.png","rb")
                await bot.send_photo(message.chat.id, photo, f"@{file[i][2]} найден!\nПроживает в {file[i][1]}")
                await sleep(3)
                flag = False
            except:
                continue
    if flag:
        await bot.send_message(message.chat.id, "К сожалению, пользователь не найден :(")
    await start_message(message)
@dp.message_handler(state=change.check_number)
async def find_number(message,state:FSMContext):
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    flag = True
    for i in file.keys():
        if file[i][0] == message.text:
            photo = open(f"image/{i}.png","rb")
            await bot.send_photo(message.chat.id, photo, f"@{file[i][2]} найден!\nПроживает в {file[i][1]}")
            flag = False
            break
    if flag:
        await bot.send_message(message.chat.id, "К сожалению, пользователь не найден :(")
    
    await start_message(message)
@dp.message_handler(state=change.adding_number)
async def add_number(message,state:FSMContext):
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    file[str(message.chat.id)][0] = message.text
    with open("base.json", "w",encoding="utf-8") as my_file:
        my_file.write(json.dumps(file))
    await bot.send_message(message.chat.id,"А теперь необходимо узнать твой город или район Москвы. Пример: «Одинцово, Сергиев Посад, Южное Бутово, Комсомольский район, Ростов-на-Дону» и т.д.\nРайоны Москвы указывать так ( Выхино, Ломоносовский район, Бибирево)\nТОЛЬКО 1 ГОРОД или РАЙОН!\nНЕ НАДО ПИСАТЬ - МОСКВА ВЫХИНО и МОСКВА ЛОМОНОСОВСКИЙ")
    await change.write_house.set()
@dp.message_handler(state=change.write_house)
async def add_house(message,state:FSMContext):
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    user = message.from_user.username
    file[str(message.chat.id)][1] = message.text
    file[str(message.chat.id)][3] = True
    with open("base.json", "w",encoding="utf-8") as my_file:
        my_file.write(json.dumps(file))
    await bot.send_message(message.chat.id,"Прикрепите одну фотографию вашего авто")
    await state.finish()
@dp.message_handler(content_types=['photo'])
async def add_photo(message,state:FSMContext):
    with open("base.json","r",encoding="utf-8") as file:
        file = file.read()
    file = json.loads(file)
    if file[str(message.chat.id)][3] == True:
        await message.photo[-1].download(f'image/{str(message.chat.id)}.png')
        await bot.send_message(message.chat.id,"Ваше авто успешно добавлено!")
        file[str(message.chat.id)][3] = False
        photo = open(f"image/{str(message.chat.id)}.png","rb")
        user = message.from_user.username
        await bot.send_photo("808223244",photo,f"@{user}\nНомер - {file[str(message.chat.id)][0]}\nРайон - {file[str(message.chat.id)][1]}")
        with open("base.json", "w",encoding="utf-8") as my_file:
            my_file.write(json.dumps(file))
        
        await start_message(message)
    
@dp.message_handler(content_types=['new_chat_members'])
async def new_member(message):
    user = message.from_user.username
    await bot.send_message(message.chat.id, f"Привет, уважаемый @{user}. Мы рады тебя приветствовать в чате Geely Coolray. Вся важная информация находится в закрепленном комментарии. \
Если у тебя есть какие-то вопросы, то ты можешь спросить их в чате или же просто поддержать беседу. \
Еще у нас есть функция поиска владельцев, которых ты встретил на улице, для этого напиши @geelyMSK_bot, а дальше следуй инструкции. Здесь же можно добавить свой авто.")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
