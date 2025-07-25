from collections import Counter
from datetime import datetime, timedelta
from pprint import pprint

from glpi_async.client import GLPIClient
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def weekly_summary():
    async with GLPIClient(
            app_token=os.getenv("GLPI_APP_TOKEN"),
            user_token=os.getenv("GLPI_USER_TOKEN"),
            base_url=os.getenv("GLPI_API_URL")
    ) as glpi:

        a = await glpi.tickets.list_open_for_user('7')
        return a


async def main():
    a = await weekly_summary()
    print(a)


if __name__ == '__main__':
    asyncio.run(main())
