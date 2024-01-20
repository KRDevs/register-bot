import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6900270837:AAEY5ubydVxT1hSZnZqcaO05gbrziDIpAxM")
dp = Dispatcher()


class RegisterState(StatesGroup):
    name = State()
    age = State()
    job = State()
    hobbi = State()
    date_year = State()
    date_month = State()
    date_day = State()


name, age, job, hobbi, date_year, date_month, date_day = "", 0, "", "", 0, 0, 0


@dp.message(Command('start'))
async def start_btn(message: types.Message):
    kb = [
        [(types.KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text="Iltimos telefon raqamingizingni yuboring", reply_markup=keyboard)


@dp.message(F.contact)
async def start_btn(message: types.Message):
    kb = [
        [(types.KeyboardButton(text="📍 Manzilni yuborish", request_location=True))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text="Iltimos manzilingizni yuboring", reply_markup=keyboard)


@dp.message(F.location)
async def get_name(message: types.Message, state=FSMContext):
    await message.answer("Ismingizni yuboring", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterState.name)


@dp.message(RegisterState.name)
async def get_name(message: types.Message, state=FSMContext):
    global name
    name = message.text
    if len(name) < 3:
        await message.answer("Siz koreyalikmisiz😳")
        await state.set_state(RegisterState.name)
    else:
        await state.set_state(RegisterState.age)
        await message.answer("Yoshingizni yuboring")


@dp.message(RegisterState.age)
async def get_name(message: types.Message, state=FSMContext):
    global age
    age = message.text
    if age.isdigit():
        await message.answer("Kasbingizni yuboring")
        await state.set_state(RegisterState.job)
    else:
        await message.answer("Ey aqlli yosh faqat raqamdan iborat bo'ladi, qaytadan kirit!!!")
        await state.set_state(RegisterState.age)


@dp.message(RegisterState.job)
async def get_name(message: types.Message, state=FSMContext):
    await message.answer("Hobbingizni yuboring")
    await state.set_state(RegisterState.hobbi)


@dp.message(RegisterState.hobbi)
async def get_name(message: types.Message, state=FSMContext):
    await message.answer("Tug'ilgan yilingizni yuboring")
    await state.set_state(RegisterState.date_year)


@dp.message(RegisterState.date_year)
async def get_name(message: types.Message, state=FSMContext):
    global date_year
    date_year = message.text
    if date_year.isdigit() and int(date_year) > 0 and int(date_year) < 2025:
        await message.answer("Tug'ilgan oyingizni yuboring")
        await state.set_state(RegisterState.date_month)
    else:
        await message.answer("Tug'ilgan yilingizni to'g'ri kiriting!!!")
        await state.set_state(RegisterState.date_year)


@dp.message(RegisterState.date_month)
async def get_name(message: types.Message, state=FSMContext):
    global date_month
    date_month = message.text
    if date_month.isdigit() and int(date_month) > 0 and int(date_month) < 13:
        await message.answer("Tug'ilgan kuningizni yuboring")
        await state.set_state(RegisterState.date_day)
    else:
        await message.answer("Tug'ilgan oyingizni to'g'ri kiriting!!!")
        await state.set_state(RegisterState.date_month)


@dp.message(RegisterState.date_day)
async def get_name(message: types.Message, state=FSMContext):
    global date_day
    date_day = message.text
    if date_day.isdigit() and int(date_month) > 0 and int(date_month) < 32:
        await message.answer(f"Xaxaxaxa 😄😄😄 {name} ma'lumotlaring mening qo'limda ertagacha 1000$ berasan🤫😋🤑")
    else:
        await message.answer("Tug'ilgan kuningizni to'g'ri kiriting!!!")
        await state.set_state(RegisterState.date_day)
    await state.clear()
user_info=f"Ismi:{name}\n Yoshi:{age}\n Tug'ilgan sanasi:{date_day}.{date_month}.{date_year}\nKasbi:{job}\nHobbisi:{hobbi}"
print(user_info)
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
