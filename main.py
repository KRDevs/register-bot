import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import create_user, edit_user, db_start

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6900270837:AAEY5ubydVxT1hSZnZqcaO05gbrziDIpAxM")
dp = Dispatcher()


class RegisterState(StatesGroup):
    name = State()
    description = State()


@dp.message(Command('start'))
async def phone_btn(message: types.Message):
    kb = [
        [(types.KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True))]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(text="Iltimos telefon raqamingizingni yuboring", reply_markup=keyboard)


@dp.message(F.contact)
async def get_name(message: types.Message, state=FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer("Ismingizni yuboring", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterState.name)


@dp.message(RegisterState.name)
async def get_age(message: types.Message, state=FSMContext):
    if len(message.text) > 3:
        await state.update_data(name=message.text)
        await state.set_state(RegisterState.description)
        await message.answer("Kurs haqida fikrlaringizni yuboring")
    else:
        await message.answer("Ismingiz 3 ta belgidan ko'p bo'lishi kerak!!!")
        await state.set_state(RegisterState.name)


@dp.message(RegisterState.description)
async def get_desc(message: types.Message, state=FSMContext):
    await state.update_data(description=message.text)
    state_date = await state.get_data()
    await message.answer(
        f"{state_date.get('name')} ma'lumotlariz muvaffaqiyatli kiritildi!!!")
    user_id = message.from_user.id
    await edit_user(state, user_id=user_id)
    await create_user(user_id=user_id, phone_number=state_date.get('phone_number'),
                      name=state_date.get('name'), description=state_date.get('description'))
    await bot.send_message(chat_id=-1001997888191,
                           text=f"Sizning ma'lumotlaringiz:\nTelefon raqami:{state_date.get('phone_number')}\n Ismi:{state_date.get('name')}")
    await state.clear()


async def main():
    await db_start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
