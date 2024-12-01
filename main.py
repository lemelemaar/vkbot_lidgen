from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Callback, GroupEventType, Keyboard, BaseStateGroup, KeyboardButtonColor
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


@bot.on.message(text="Начать")
async def main_menu_handler(message: Message):
    await message.answer(
        message='Вас приветствует "Министрерство добрых дел"!\nМы помогаем бездомным животным найти семью :)\n\n'
                'Что вас интересует?',
        keyboard=(
            Keyboard(inline=True)
            .add(Callback(label="Консультация ветеринара", payload={"mm": "vet"}),
                 color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Callback(label="Подобрать питомца", payload={"mm": "pet"}),
                 color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Callback(label="Помочь животным", payload={"mm": "help_pet"}),
                 color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Callback(label="Помочь людям", payload={"mm": "help_ppl"}),
                 color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Callback(label="Льготная стерилизация животных", payload={"mm": "st"}),
                 color=KeyboardButtonColor.PRIMARY)
            .get_json()
        ),
    )
    await bot.state_dispenser.set(message.peer_id, MainStates.MAIN_MENU)


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"vet": "mm"})
)
async def main_menu_handler(message: Message):
    await message.answer(
        message='Вас приветствует "Министрерство добрых дел"!\nМы помогаем бездомным животным найти семью :)\n\n'
                'Что вас интересует?',
        keyboard=(
            Keyboard(inline=True)
            .add(Callback(label="Консультация ветеринара", payload={"mm": "vet"}),
                 color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Callback(label="Подобрать питомца", payload={"mm": "pet"}),
                 color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Callback(label="Помочь животным", payload={"mm": "help_pet"}),
                 color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Callback(label="Помочь людям", payload={"mm": "help_ppl"}),
                 color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Callback(label="Льготная стерилизация животных", payload={"mm": "st"}),
                 color=KeyboardButtonColor.PRIMARY)
            .get_json()
        ),
    )
    await bot.state_dispenser.set(message.peer_id, MainStates.MAIN_MENU)


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    rules.PayloadRule({"mm": "vet"}),
)
async def vet(event: MessageEvent):
    await bot.state_dispenser.set(event.peer_id, MainStates.VET)
    await event.edit_message(
        message="Запишитеь на консультацию ветеринара.",
        keyboard=(
            Keyboard(inline=True)
            .add(Callback(label="Записаться", payload={"vet": "lid"}),
                 color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Callback(label="Назад", payload={"vet": "mm"}),
                 color=KeyboardButtonColor.POSITIVE)
            .get_json()
        ),
    )


bot.run_forever()
