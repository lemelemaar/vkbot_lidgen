from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Callback, GroupEventType, Keyboard, BaseStateGroup, KeyboardButtonColor, Text
from dotenv import load_dotenv
import logging
import os


load_dotenv()
bot = Bot(token=os.getenv("VKAPI_TOKEN"))
logging.basicConfig(level=logging.INFO)


class MainStates(BaseStateGroup):
    MAIN_MENU = "main_menu"
    VET = "vet"
    PET = "pet"
    HELP_PET = "help_pet"
    HELP_PPL = "help_ppl"
    STERILIZATION = "sterilization"
    LID_VET = "lid_vet"
    LID_VET_OK = "lid_vet_ok"


@bot.on.private_message(state=None)
@bot.on.private_message(
    text=["Назад", "Назад".upper(), "Назад".lower()],
    state=[
        MainStates.VET, MainStates.PET,
        MainStates.HELP_PET, MainStates.HELP_PPL,
        MainStates.STERILIZATION
    ]
)
async def main_menu_handler(message: Message):
    await bot.state_dispenser.set(message.peer_id, MainStates.MAIN_MENU)
    await message.answer(
        message='Вас приветствует организация "Министрерство добрых дел"!\n'
                'Мы помогаем бездомным животным найти семью :)\n\nЧто вас интересует?',
        keyboard=(
            Keyboard(inline=False)
            .add(Text(label="Консультация ветеринара"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text(label="Подобрать питомца"), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text(label="Помочь животным"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text(label="Помочь людям"), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text(label="Льготная стерилизация животных"), color=KeyboardButtonColor.PRIMARY)
            .get_json()
        ),
    )


@bot.on.private_message(
    text=[
        "Консультация ветеринара", "Консультация ветеринара".upper(),
        "Консультация ветеринара".lower()
    ],
    state=MainStates.MAIN_MENU
)
async def vet(message: Message):
    await bot.state_dispenser.set(message.peer_id, MainStates.VET)
    await message.answer(
        message="Хотите записаться на консультацию ветеринара?",
        keyboard=(
            Keyboard(inline=False)
            .add(Text(label="Записаться"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text(label="Назад"), color=KeyboardButtonColor.POSITIVE)
            .get_json()
        ),
    )


@bot.on.private_message(text=["Записаться", "Записаться".upper(), "Записаться".lower()], state=MainStates.VET)
async def lid(message: Message):
    await bot.state_dispenser.set(message.peer_id, MainStates.LID_VET)
    await message.answer(
        message="Введите свой номер телефона. Мы свяжемся с вами при первой появившейся возможности.",
        keyboard=(
            Keyboard(inline=False)
            .add(Text(label="Назад"), color=KeyboardButtonColor.POSITIVE)
            .get_json()
        ),
    )


@bot.on.private_message(state=MainStates.LID_VET, length=10)
async def tel(message: Message):
    await message.reply(
        message="Это ваш номер телефона? Подтвердите.",
        keyboard=(
            Keyboard(inline=False)
            .add(Text(label="Да"), color=KeyboardButtonColor.PRIMARY)
            .add(Text(label="Назад"), color=KeyboardButtonColor.POSITIVE)
            .get_json()
        ),
    )


@bot.on.private_message(state=MainStates.LID_VET, text=["Да", "Да".upper(), "Да".lower()])
async def tel_ok(message: Message):
    await bot.state_dispenser.set(message.peer_id, MainStates.LID_VET_OK)
    m = await bot.api.messages.get_by_id(message_ids=message.id-2)
    await bot.api.messages.send(
        peer_id=2000000001,
        message=f"{m.items[0].text}",
        random_id=0
    )
    await message.answer("Спасибо! Мы позвоним вам при первой возможности :)")


bot.run_forever()
