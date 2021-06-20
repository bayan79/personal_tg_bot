import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from api.binance import Binance
from api.tinkoff import Tinkoff
from api.tinkoff.report import StocksReport

load_dotenv()


class Config:
    TINKOFF_API_TOKEN = os.getenv('TINKOFF_API_TOKEN')
    BOT_TOKEN = os.getenv('BOT_TOKEN') or ''


logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher(bot)

tinkoff = Tinkoff()
binance = Binance()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['stocks_report'])
async def stocks_report(message: types.Message):
    user = tinkoff.get_user_accounts()
    report = StocksReport(user=user)
    await message.reply(report.render(), parse_mode='HTML', reply=False)


@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    user = tinkoff.get_user_accounts()
    report = StocksReport(user=user)

    capital = binance.get_user_balance()
    capital_report = f"Binance: ${sum(binance.get_price(coin.coin).price * coin.free for coin in capital.__root__):.4f}"
    await message.reply(report.render() + '\n\n' + capital_report, parse_mode='HTML', reply=False)


@dp.message_handler(regexp='(^cat[s__]?$|puss)')
async def cats(message: types.Message):
    with open('cat.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
