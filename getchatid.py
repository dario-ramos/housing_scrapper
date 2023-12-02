#!/usr/bin/env python3

import asyncio
import telegram

async def main():
    bot = telegram.Bot('<TELEGRAM_TOKEN_>')
    async with bot:
        print((await bot.get_updates())[0])

if __name__ == '__main__':
    asyncio.run(main())

# TODO: Fix providers, especially the ones that use ChromeDriver
