#!/usr/bin/env python3

import telegram

bot = telegram.Bot(token='1958942562:AAGKDfy2S7vcXj3cFe0I1-0Hevq8ayM-9U0')
print([u.message.chat.id for u in bot.get_updates()])
